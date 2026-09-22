# Informe — Ciber-G9

Última actualización: Oriol, Nacho y Luisda (preguntas 1-9)

## 1. ¿Por qué el segundo push del apartado 2.2 fue rechazado? ¿Qué dos operaciones hace `git pull` por debajo?

El push de Luisda fue rechazado ([rejected] main -> main (fetch first))
porque en GitHub ya estaba el commit de Nacho y en su copia local no. Git no deja
subir si eso borra trabajo ajeno del remoto.

git pull hace git fetch (descarga lo nuevo de origin/main) y git merge
(lo fusiona con el main local). Como usamos pull.rebase false, crea un merge
commit: 3457576 y 9383468 en nuestro historial.

## 2. En vuestro historial, señalad un merge *fast-forward* y un *merge commit*. ¿Qué los diferencia?

Fast-forward: git merge contacto-a (a210d87..f841733). main no había
avanzado, así que Git solo movió el puntero, sin crear commit.

Merge commit: c06744f (Merge branch 'contacto-b'). Las dos ramas habían avanzado
por separado, así que Git creó un commit nuevo con dos padres. El fast-forward deja
el historial lineal y no puede dar conflicto; el merge commit sí.

## 3. ¿Por qué rellenar filas distintas de la tabla no dio conflicto y cambiar `Última revisión` sí?

Git compara cada rama con el ancestro común. Si los cambios están en zonas
distintas del fichero, los combina solo; si dos ramas cambian la misma línea, no
sabe cuál elegir y marca conflicto. Las filas del README se hicieron en commits
seguidos sobre main, sin ramas divergentes, mientras que Última revisión la
cambiaron dos ramas a la vez. También da conflicto si las líneas están pegadas, como
nos pasó con los ítems del checklist en el 2.2.

## 4. Pegad el mensaje de error del push a `main` protegida y explicad qué regla lo ha bloqueado.

- remote: error: GH006: Protected branch update failed for refs/heads/main.
  remote: - Changes must be made through a pull request.
  ! [remote rejected] main -> main (protected branch hook declined)

- Lo bloqueó la regla Require a pull request before merging de main. Como
marcamos Do not allow bypassing, falló incluso para Oriol, que es Admin.

## 5. ¿Qué comando sacó `.env` del control de versiones sin borrarlo? ¿Por qué la contraseña sigue siendo un problema y qué haríais en un proyecto real?
- Con git rm --cached .env, que lo quita de Git sin borrarlo del disco, más
la línea .env en .gitignore (PR #5).

- Sigue siendo un problema porque la contraseña sigue en el historial (se ve en el
commit d86f63a), en los clones y en la PR, y el repo es público. En un proyecto
real, lo primero es cambiar la contraseña y revisar accesos. Después se puede
limpiar el historial con git filter-repo, pero eso no deshace la exposición.

## 6. ¿Qué hace mejor GitHub Desktop que la terminal, y qué no puede hacer? ¿Con cuál habéis entendido mejor el conflicto?

- Desktop muestra mejor el diff y los conflictos, y avisa antes del commit de
que main está protegida. En cambio, no permite configurar la protección ni los
roles, ni revisar PR (eso lo hicimos en la web), ni ver el grafo o usar
git rm --cached (eso, en la terminal). Además coló un .DS_Store y el editor nos
escapó el Markdown. El conflicto lo entendimos mejor en la terminal, porque se ven
los marcadores.

## 7. Roles: ¿qué puede hacer un Maintain que no pueda un Write? ¿Quién podría haber quitado la protección de `main`?

Write (Luisda) puede crear ramas, hacer push a ramas no protegidas y
abrir, revisar y fusionar PR. Maintain (Nacho) además gestiona ajustes del repo
como la descripción, la wiki, issues o los tipos de merge, pero no la seguridad ni
el acceso. La protección de main solo la podía quitar Oriol, que es Admin.

## 8. Si mañana un miembro sube un force push a `main`, ¿qué se pierde y qué lo impide en vuestro repositorio?

Se perdería todo lo que haya en el main de GitHub y no esté en la copia de
quien hace el force push, como merges de PR o commits de otros, y los demás
quedarían desincronizados. Lo impide la regla de protección: Allow force pushes
desmarcado y Do not allow bypassing activado.

## 9. En la Fase 1 compartíais un portátil y en la Fase 2 cada uno tenía el suyo. ¿Qué diferencia práctica tiene eso para la identidad del autor de cada commit y para cómo aparecen los conflictos?

Con un portátil, cada uno tenía que cambiar `git config --local` antes de su commit y era fácil equivocarse: un commit salió con un correo de ejemplo y lo corregimos con `--amend --reset-author`. Con portátiles separados, la identidad es automática con `--global`. Los conflictos, en la Fase 1, salían al hacer merge entre ramas locales; en la Fase 2 salen al sincronizar (push rechazado, `pull` o PR), así que hace falta más coordinación.