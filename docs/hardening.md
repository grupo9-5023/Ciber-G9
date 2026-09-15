# Checklist de hardening del servidor web

Estado global: 2/3 completado

- [x] Forzar HTTPS con redirección 301 y cabecera HSTS
- [x] Ocultar la versión del servidor en cabeceras y páginas de error
- [x] Desactivar el listado de directorios — Apache: Options -Indexes; Nginx: autoindex off. Se comprueba entrando en una carpeta sin index.html