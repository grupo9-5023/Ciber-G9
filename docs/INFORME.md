# Informe — Ciber-G9

Última actualización: Luisda (preguntas 7-9)

## 1. ¿Por qué el segundo push del apartado 2.2 fue rechazado? ¿Qué dos operaciones hace `git pull` por debajo?

## 2. En vuestro historial, señalad un merge *fast-forward* y un *merge commit*. ¿Qué los diferencia?

## 3. ¿Por qué rellenar filas distintas de la tabla no dio conflicto y cambiar `Última revisión` sí?

## 4. Pegad el mensaje de error del push a `main` protegida y explicad qué regla lo ha bloqueado.

## 5. ¿Qué comando sacó `.env` del control de versiones sin borrarlo? ¿Por qué la contraseña sigue siendo un problema y qué haríais en un proyecto real?

## 6. ¿Qué hace mejor GitHub Desktop que la terminal, y qué no puede hacer? ¿Con cuál habéis entendido mejor el conflicto?
------------
## 7. Roles: ¿qué puede hacer un Maintain que no pueda un Write? ¿Quién podría haber quitado la protección de `main`?

Write (Luisda) puede crear ramas, hacer push a ramas no protegidas y
abrir, revisar y fusionar PR. Maintain (Nacho) además gestiona ajustes del repo
como la descripción, la wiki, issues o los tipos de merge, pero no la seguridad ni
el acceso. La protección de main solo la podía quitar Oriol, que es Admin.
------------
## 8. Si mañana un miembro sube un force push a `main`, ¿qué se pierde y qué lo impide en vuestro repositorio?

Se perdería todo lo que haya en el main de GitHub y no esté en la copia de
quien hace el force push, como merges de PR o commits de otros, y los demás
quedarían desincronizados. Lo impide la regla de protección: Allow force pushes
desmarcado y Do not allow bypassing activado.
-----------
## 9. En la Fase 1 compartíais un portátil y en la Fase 2 cada uno tenía el suyo. ¿Qué diferencia práctica tiene eso para la identidad del autor de cada commit y para cómo aparecen los conflictos?

Se perdería todo lo que haya en el main de GitHub y no esté en la copia de
quien hace el force push, como merges de PR o commits de otros, y los demás
quedarían desincronizados. Lo impide la regla de protección: Allow force pushes
desmarcado y Do not allow bypassing activado.