# Pipeline CI/CD con Jenkins — Grupo 9

Todo se ejecuta en el Ubuntu Server (VM de Proxmox, `10.30.212.109`), la misma
máquina donde ya están Docker y las webs del profesor.

```
commit/PR en GitHub ──(pollSCM cada 2 min)──> Jenkins
  1. Preparación
  2. SAST  - Semgrep (p/php, p/owasp-top-ten, p/secrets)   -> para si hay ERROR
  3. Build de las 3 imágenes (deploy/Dockerfile)
  4. Deploy a test        (puertos 55340 / 55350 / 55360)
  5. DAST  - OWASP ZAP full scan de las 3 webs              -> para si hay alerta High
  6. Deploy a preproducción (puertos 56340 / 56350 / 56360)
  post: se borra test, se archivan y publican los informes
```

| Web | Carpeta | Test | Preproducción | Profesor (no se toca) |
|---|---|---|---|---|
| Star Wars | `web-estrella-de-la-muerte` | 55340 | 56340 | 54340 |
| Mordor | `web-mordor` | 55350 | 56350 | 54350 |
| Star Trek | `StarTrek` | 55360 | 56360 | 54360 |

## Ficheros

| Fichero | Para qué |
|---|---|
| `Jenkinsfile` | Etapas del pipeline |
| `docker-compose.yml` | Las 3 webs + 3 MySQL. Se usa con `-p g9-test` y `-p g9-preprod` |
| `deploy/Dockerfile` | Imagen PHP 8.2 + Apache. Copia el código dentro, no publica `init.sql`, solo deja escribir en la carpeta de subidas |
| `deploy/sql/deathstar.sql` | BD de Star Wars (hay que generarla, paso 0) |
| `ci/security_gate.py` | Lee los JSON de Semgrep/ZAP y decide si el pipeline sigue |
| `*/db.php` | La contraseña de MySQL ya no está en el código: llega por la variable `DB_PASSWORD` |

---

## Paso 0 — Base de datos de Star Wars (una sola vez)

Mordor y Star Trek tienen `init.sql`; Star Wars no. Se saca de la BD del profesor, que está corriendo:

```bash
cd ~/Ciber-G9    # o donde tengáis clonado el repo
mkdir -p deploy/sql
sudo docker exec mysql_examen_1 mysqldump -uroot -proot_pass_examen1 --databases deathstar > deploy/sql/deathstar.sql
head -30 deploy/sql/deathstar.sql   # debe tener CREATE DATABASE ... deathstar y CREATE TABLE
```

Subidlo al repo dentro de la rama `feature/jenkins-pipeline` (paso 6).

## Paso 1 — Comprobaciones previas en el servidor

```bash
docker compose version     # Compose v2 (necesario para --wait)
python3 --version          # lo usa ci/security_gate.py
sudo ss -ltnp | grep -E ':8080|:5[56]3[4-6]0' || echo "puertos libres"
```

Si el 8080 está ocupado (por ejemplo, por ZAP), Jenkins irá en el 8081 (paso 2).

## Paso 2 — Instalar Jenkins (documentación oficial, versión LTS)

Java 21 primero:

```bash
sudo apt update
sudo apt install fontconfig openjdk-21-jre
java -version
```

Repositorio e instalación:

```bash
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins
```

Si hay que cambiar el puerto: `sudo systemctl edit jenkins` y añadir:

```
[Service]
Environment="JENKINS_PORT=8081"
```

Arrancar y dar acceso a Docker al usuario `jenkins`:

```bash
sudo usermod -aG docker jenkins
sudo systemctl enable --now jenkins
sudo systemctl restart jenkins        # para que coja el grupo docker
sudo -u jenkins docker ps             # no debe dar "permission denied"
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

> Nota de seguridad para la memoria: estar en el grupo `docker` equivale a ser root
> en la máquina. Es aceptable en un laboratorio con un solo servidor; en producción
> se usarían agentes separados.

## Paso 3 — Configuración inicial (navegador: `http://10.30.212.109:8080`)

1. Pegar la contraseña inicial, elegir **Install suggested plugins**.
2. Crear un usuario administrador propio (no seguir con `admin` + contraseña inicial).
3. **Manage Jenkins → Plugins → Available**: instalar **HTML Publisher** y **Warnings**
   (Warnings Next Generation). Reiniciar.
4. **Manage Jenkins → Security**:
   - Security Realm: *Jenkins' own user database*, sin permitir registro.
   - Authorization: *Logged-in users can do anything*, sin marcar acceso de lectura anónimo
     (o *Matrix-based* si queréis dar permisos distintos a cada miembro).
   - CSRF Protection: dejarla activada (viene por defecto).
5. **Manage Jenkins → Credentials → System → Global → Add Credentials**:
   - Kind: **Secret text**
   - Secret: la contraseña root que queráis para las BD de test/preprod (una nueva, no la del profesor)
   - ID: **`g9-db-root-password`** (exacto, lo usa el Jenkinsfile)

Haced capturas de cada pantalla: son el apartado "Configuracions de Jenkins" de la memoria.

## Paso 4 — Crear el job

**New Item → nombre `Ciber-G9-pipeline` → Pipeline → OK**

- *Pipeline → Definition*: **Pipeline script from SCM**
- SCM: **Git**, Repository URL: `https://github.com/grupo9-5023/Ciber-G9.git`
  (repo público: no hace falta credencial)
- Branch Specifier: `*/main`
- Script Path: `Jenkinsfile`
- Guardar.

## Paso 5 — Primera ejecución

Pulsar **Build Now** una vez a mano. Hace falta porque Jenkins solo lee el bloque
`triggers { pollSCM(...) }` del Jenkinsfile después de la primera ejecución. A partir
de ahí, cada commit en `main` lanza el pipeline solo, en unos 2 minutos como máximo.

Al terminar, en la página del build aparecen:
- **Informe ZAP (DAST)**: los tres informes HTML de ZAP.
- **Semgrep (SAST)**: los hallazgos de Semgrep (plugin Warnings).
- **Build Artifacts**: `reports/` con `semgrep.json`, `semgrep.sarif` y `zap/*.html|json`.

El informe HTML de ZAP puede verse sin estilos dentro de Jenkins (la política de
seguridad de contenido de Jenkins bloquea su CSS/JS). Es normal: el original completo
está en *Build Artifacts*.

## Paso 6 — Subir estos ficheros por el flujo de la práctica

`main` está protegida, así que entran por PR:

```bash
git switch -c feature/jenkins-pipeline   # si no existe ya
git add Jenkinsfile docker-compose.yml .dockerignore deploy ci docs/JENKINS.md */db.php
git commit -m "ci: pipeline Jenkins con SAST, DAST y despliegue a preproducción"
git push -u origin feature/jenkins-pipeline
```

PR → revisión de un compañero → merge → Jenkins lo detecta.

---

## Puertas de seguridad (criterio)

- **SAST**: el pipeline para si Semgrep da algún hallazgo de severidad `ERROR`.
  Los `WARNING`/`INFO` (por ejemplo, cookie sin `Secure`, que no se puede arreglar sin HTTPS)
  quedan en el informe pero no bloquean.
- **DAST**: el pipeline para si ZAP da alguna alerta de riesgo **High**.
  Medium/Low (cabeceras CSP, anti-CSRF...) quedan en el informe.
- Limitación (pregunta 6 del AC6): ZAP escanea sin autenticarse, así que las zonas
  con login solo se prueban en la parte pública.

Para cambiar el criterio: `ci/security_gate.py`.

## Guion del vídeo (commit → preproducción)

1. Enseñar Jenkins: job, credencial `g9-db-root-password` (sin revelar el valor), plugins.
2. **Commit vulnerable**: en una rama, reintroducir un fallo que Semgrep marque como ERROR
   (p. ej. volver a concatenar `$_POST['ip']` en `shell_exec` en `admin/terminal.php`).
   PR → aprobación → merge.
3. Jenkins arranca solo → **SAST en rojo** → el pipeline para y no llega a preproducción.
   Enseñar el log de la puerta y el informe de Semgrep.
4. **Commit de corrección** (revertir el cambio) → PR → merge.
5. Jenkins: SAST verde → build → test → **DAST** (ZAP) → **preproducción**.
6. Abrir los informes de ZAP desde el build y las webs en `:56340`, `:56350`, `:56360`.

## Problemas típicos

| Síntoma | Causa / solución |
|---|---|
| `permission denied ... docker.sock` | Falta `usermod -aG docker jenkins` + reiniciar Jenkins |
| `Falta deploy/sql/deathstar.sql` | Paso 0 |
| `Falta DB_ROOT_PASSWORD` / credencial no encontrada | El ID de la credencial no es exactamente `g9-db-root-password` |
| `No such DSL method 'publishHTML'` o `'recordIssues'` | Falta HTML Publisher o Warnings |
| ZAP no puede escribir el informe | La carpeta `reports/zap` necesita `chmod 777` (lo hace la etapa Preparación) |
| `port is already allocated` | Algo ocupa 5534x/5634x: `sudo ss -ltnp` |
| El pipeline no arranca solo tras un commit | No se ha hecho la primera ejecución manual (paso 5) |
| El pipeline tarda ~1 hora | Normal: el full scan de ZAP (ataque activo) tarda ~20 min por web. En el vídeo, cortad o acelerad esa parte |
