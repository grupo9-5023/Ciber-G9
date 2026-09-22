# Informe — Ciber-G9

Última actualización: Nacho (Preguntas 4-6)

## 1. ¿Por qué el segundo push del apartado 2.2 fue rechazado? ¿Qué dos operaciones hace `git pull` por debajo?

## 2. En vuestro historial, señalad un merge *fast-forward* y un *merge commit*. ¿Qué los diferencia?

## 3. ¿Por qué rellenar filas distintas de la tabla no dio conflicto y cambiar `Última revisión` sí?

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

## 8. Si mañana un miembro sube un force push a `main`, ¿qué se pierde y qué lo impide en vuestro repositorio?

## 9. En la Fase 1 compartíais un portátil y en la Fase 2 cada uno tenía el suyo. ¿Qué diferencia práctica tiene eso para la identidad del autor de cada commit y para cómo aparecen los conflictos?
