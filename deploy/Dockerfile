# Imagen común para las tres webs (misma base que el Dockerfile del profesor).
# El código se copia DENTRO de la imagen: lo que se prueba en test es
# exactamente lo que se despliega en preproducción.
FROM php:8.2-apache

RUN docker-php-ext-install mysqli pdo pdo_mysql && docker-php-ext-enable mysqli

# No anunciar versiones de PHP ni de Apache en las cabeceras (alerta High de ZAP
# "PHP Version with Known Vulnerabilities" y Low "X-Powered-By" / "Server")
RUN echo 'expose_php = Off' > /usr/local/etc/php/conf.d/security.ini \
 && sed -ri 's/^ServerTokens .*/ServerTokens Prod/; s/^ServerSignature .*/ServerSignature Off/' \
      /etc/apache2/conf-available/security.conf

# SITE_DIR: carpeta de la web en el repo (web-mordor, StarTrek, ...)
# WRITABLE_DIR: única carpeta donde www-data puede escribir (subidas)
ARG SITE_DIR
ARG WRITABLE_DIR=""

COPY ${SITE_DIR}/ /var/www/html/

# - init.sql no se publica en la web (fuga de credenciales, ver informe Mordor B.1)
# - el resto del código queda como root: www-data solo escribe en WRITABLE_DIR
RUN rm -f /var/www/html/init.sql \
 && if [ -n "$WRITABLE_DIR" ]; then \
      mkdir -p "/var/www/html/$WRITABLE_DIR" \
      && chown www-data:www-data "/var/www/html/$WRITABLE_DIR"; \
    fi
