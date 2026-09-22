# Informe — Ciber-G9

Última actualización: Oriol (preguntas 1-3)

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

## 5. ¿Qué comando sacó `.env` del control de versiones sin borrarlo? ¿Por qué la contraseña sigue siendo un problema y qué haríais en un proyecto real?

## 6. ¿Qué hace mejor GitHub Desktop que la terminal, y qué no puede hacer? ¿Con cuál habéis entendido mejor el conflicto?

## 7. Roles: ¿qué puede hacer un Maintain que no pueda un Write? ¿Quién podría haber quitado la protección de `main`?

## 8. Si mañana un miembro sube un force push a `main`, ¿qué se pierde y qué lo impide en vuestro repositorio?

## 9. En la Fase 1 compartíais un portátil y en la Fase 2 cada uno tenía el suyo. ¿Qué diferencia práctica tiene eso para la identidad del autor de cada commit y para cómo aparecen los conflictos?
