// Pipeline CI/CD - Grupo 9
// commit en GitHub -> SAST (Semgrep) -> build -> test -> DAST (OWASP ZAP) -> preproducción
//
// Plugins necesarios además de los sugeridos: HTML Publisher, Warnings Next Generation.
// Credencial necesaria (Secret text): g9-db-root-password

pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '15'))
        disableConcurrentBuilds()   // test y preprod usan puertos fijos
        timeout(time: 150, unit: 'MINUTES')   // ZAP full scan: ~20 min por web
    }

    // El servidor está en la red del centro: GitHub no puede llamar a Jenkins
    // (webhook), así que Jenkins pregunta a GitHub cada 2 minutos.
    triggers {
        pollSCM('H/2 * * * *')
    }

    environment {
        SERVER_IP        = '10.30.212.53'
        IMAGE_TAG        = "${env.BUILD_NUMBER}"
        DB_ROOT_PASSWORD = credentials('g9-db-root-password')
        SEMGREP_IMAGE    = 'semgrep/semgrep'
        ZAP_IMAGE        = 'ghcr.io/zaproxy/zaproxy:stable'
    }

    stages {
        stage('Preparación') {
            steps {
                sh '''
                    rm -rf reports && mkdir -p reports/zap
                    # ZAP escribe como usuario "zap" del contenedor
                    chmod 777 reports/zap
                    test -f deploy/sql/deathstar.sql || { echo "Falta deploy/sql/deathstar.sql (ver docs/JENKINS.md)"; exit 1; }
                    git log -1 --pretty='Commit %h de %an: %s'
                '''
            }
        }

        stage('SAST - Semgrep') {
            steps {
                sh '''
                    docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp \
                        -v "$WORKSPACE:/src" -w /src "$SEMGREP_IMAGE" \
                        semgrep scan \
                            --config p/php --config p/owasp-top-ten --config p/secrets \
                            --exclude docs --exclude reports --exclude '*.pdf' \
                            --json-output=reports/semgrep.json \
                            --sarif-output=reports/semgrep.sarif \
                            .
                    python3 ci/security_gate.py semgrep reports/semgrep.json
                '''
            }
        }

        stage('Build imágenes') {
            environment {   // el compose exige los puertos aunque solo construya
                PORT_STARWARS = '55340'
                PORT_MORDOR   = '55350'
                PORT_STARTREK = '55360'
            }
            steps {
                sh 'docker compose -p g9-test build'
            }
        }

        stage('Deploy a test') {
            environment {
                PORT_STARWARS = '55340'
                PORT_MORDOR   = '55350'
                PORT_STARTREK = '55360'
            }
            steps {
                sh '''
                    docker compose -p g9-test down -v --remove-orphans || true
                    docker compose -p g9-test up -d --no-build --wait --wait-timeout 300
                    for p in $PORT_STARWARS $PORT_MORDOR $PORT_STARTREK; do
                        curl -fsS -o /dev/null "http://$SERVER_IP:$p/" && echo "test :$p OK"
                    done
                '''
            }
        }

        stage('DAST - OWASP ZAP') {
            steps {
                sh '''
                    scan() {  # $1 = nombre del informe, $2 = puerto
                        rc=0
                        docker run --rm -v "$WORKSPACE/reports/zap:/zap/wrk/:rw" "$ZAP_IMAGE" \
                            zap-full-scan.py -t "http://$SERVER_IP:$2" -m 2 -I \
                            -r "$1.html" -J "$1.json" || rc=$?
                        # 0-2 = escaneo hecho (con o sin alertas); 3 = error de ZAP
                        [ "$rc" -le 2 ] || { echo "ZAP falló en $1 (código $rc)"; exit "$rc"; }
                    }
                    scan starwars 55340
                    scan mordor   55350
                    scan startrek 55360
                    python3 ci/security_gate.py zap reports/zap/starwars.json reports/zap/mordor.json reports/zap/startrek.json
                '''
            }
        }

        stage('Deploy a preproducción') {
            environment {
                PORT_STARWARS = '56340'
                PORT_MORDOR   = '56350'
                PORT_STARTREK = '56360'
            }
            steps {
                // Mismas imágenes (IMAGE_TAG) que han pasado SAST y DAST: no se recompila
                sh '''
                    docker compose -p g9-preprod up -d --no-build --wait --wait-timeout 300
                    for p in $PORT_STARWARS $PORT_MORDOR $PORT_STARTREK; do
                        curl -fsS -o /dev/null "http://$SERVER_IP:$p/" && echo "preprod :$p OK"
                    done
                '''
            }
        }
    }

    post {
        always {
            // El entorno de test solo existe durante el pipeline
            sh '''
                PORT_STARWARS=55340 PORT_MORDOR=55350 PORT_STARTREK=55360 \
                    docker compose -p g9-test down -v --remove-orphans || true
            '''
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            script {
                if (fileExists('reports/semgrep.sarif')) {
                    recordIssues(enabledForFailure: true, tools: [sarif(pattern: 'reports/semgrep.sarif', id: 'semgrep', name: 'Semgrep (SAST)')])
                }
            }
            publishHTML(target: [
                reportName: 'Informe ZAP (DAST)',
                reportDir: 'reports/zap',
                reportFiles: 'starwars.html,mordor.html,startrek.html',
                reportTitles: 'Star Wars,Mordor,Star Trek',
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true
            ])
        }
        success {
            echo "Desplegado en preproducción: http://${SERVER_IP}:56340 | :56350 | :56360"
        }
        failure {
            echo 'Pipeline parado: revisa la puerta de seguridad en el log y los informes del build.'
        }
    }
}
