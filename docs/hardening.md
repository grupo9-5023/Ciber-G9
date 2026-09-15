Checklist de hardening del servidor web

Estado global: 2/3 completado

[x] Forzar HTTPS con redirección
[x] Ocultar la versión del servidor en cabeceras y páginas de error — Apache: ServerTokens Prod y ServerSignature Off; Nginx: server_tokens off
[x] Desactivar el listado de directorios — Apache: Options -Indexes; Nginx: autoindex off. Se comprueba entrando en una carpeta sin index.html
