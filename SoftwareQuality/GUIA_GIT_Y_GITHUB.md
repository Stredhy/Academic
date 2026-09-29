# Guía de trabajo con Git y GitHub – Mis Trapitos

Esta guía es para **todo el equipo**. Si todos siguen el mismo ciclo, el Project (tablero) se llena solo y el dashboard final tiene historial real de quién hizo qué y cuándo.

---

## 0. Las reglas de oro (léelas primero)

1. **Todo el trabajo ocurre en `SQEquipo3/Trapitos`.** Es el repo donde están los issues y el Project.
2. **Nadie abre Pull Requests hacia `Blises/Trapitos`.** Ese es el repo de origen del fork; no se toca hasta la entrega final.
3. **Nunca se trabaja directo en `main`.** Siempre en una rama.
4. **Una tarea = un issue = una rama = un Pull Request.**
5. **Todo Pull Request lleva `Closes #N`** en la descripción (con el número real del issue).
6. **La tarjeta del Project se mueve el mismo día** que cambia el estado real.
7. **No se copian ni pegan archivos a mano de una rama a otra.** Para juntar trabajo se usa `merge`.

---

## 1. Cómo reconocer el repo correcto (fork vs. original)

Nuestro repo es un **fork**. Eso significa que existen dos repos parecidos:

| Repo | Para qué sirve | ¿Se usa? |
|---|---|---|
| `SQEquipo3/Trapitos` | Donde están issues, Project y todo el trabajo | **SÍ, siempre** |
| `Blises/Trapitos` | Repo original (de origen del fork) | **NO, no tocar** |

### Cómo saber en cuál estás

1. Mira la **barra de direcciones** del navegador. Debe empezar con:
   ```
   github.com/SQEquipo3/Trapitos
   ```
2. Mira **arriba a la izquierda** de la página: debe decir `SQEquipo3 / Trapitos`.
3. Debajo del nombre `Trapitos` debe aparecer el texto pequeño **"forked from Blises/Trapitos"**. Eso confirma que estás en el fork correcto.

Si en cualquier momento ves `Blises` en la barra de direcciones o arriba a la izquierda, **para y regresa** a `github.com/SQEquipo3/Trapitos`.

---

## 1.1 Configuración inicial (una sola vez por persona)

### A) Ver a qué repo apunta tu carpeta local

Abre una terminal dentro de la carpeta del proyecto (en VS Code: menú **Terminal → New Terminal**) y escribe:

```bash
git remote -v
```

Debe salir algo así:

```
origin  https://github.com/SQEquipo3/Trapitos.git (fetch)
origin  https://github.com/SQEquipo3/Trapitos.git (push)
```

### B) Si dice `Blises` en lugar de `SQEquipo3`

Corrígelo con:

```bash
git remote set-url origin https://github.com/SQEquipo3/Trapitos.git
git fetch origin
```

Vuelve a correr `git remote -v` para confirmar.

### C) Si no tienes el proyecto en tu computadora

```bash
git clone https://github.com/SQEquipo3/Trapitos.git
cd Trapitos
```

---

## 2. El ciclo completo de una tarea (paso a paso)

### PASO 1 – Que exista el issue

Sin issue no hay historial en el dashboard. Antes de programar, verifica que el issue tenga:

- **Assignee** (quién lo hace)
- **Sprint** (Iteration)
- **Story Points**
- **Start date** y **Target date**
- **Parent issue** (la épica, por ejemplo #9)
- **Label** (`enhancement`, `bug`, `docs`, `test`)

Para crear uno nuevo: en `github.com/SQEquipo3/Trapitos` → pestaña **Issues** → botón verde **New issue** → usa la plantilla de user story.

---

### PASO 2 – Empezar la tarea

**2.1 Mover la tarjeta a "In Progress"**

1. Abre el Project: `github.com/orgs/SQEquipo3/projects/3`.
2. Busca tu tarjeta.
3. **Arrástrala** a la columna **In Progress**.

> Este paso es manual. Ningún workflow lo hace solo.

**2.2 Crear la rama desde el issue**

1. Abre el issue (clic en el título de la tarjeta).
2. En la barra derecha, busca la sección **Development**.
3. Clic en **Create a branch**.
4. En **Branch source** elige **`main`**. (Importante: no otra rama.)
5. Deja el nombre que propone GitHub (por ejemplo `14-integrar-main-y-utils`) o ponle uno corto y claro.
6. Selecciona **Checkout locally** y clic en **Create branch**.

**2.3 Traer la rama a tu computadora**

En la terminal:

```bash
git fetch origin
git checkout 14-integrar-main-y-utils
git pull origin main
```

(Usa el nombre real de tu rama.)

Verifica en qué rama estás:

```bash
git branch
```

La rama con `*` es en la que estás parado. Debe ser la tuya, **no `main`**.

---

### PASO 3 – Trabajar y guardar cambios

Trabaja normal en VS Code. Cuando tengas un avance:

```bash
git status
git add .
git commit -m "Crea utils.py con constantes compartidas (#14)"
git push origin 14-integrar-main-y-utils
```

Reglas para los commits:

- **Chicos y frecuentes**, no uno gigante al final.
- **Siempre con el número del issue** (`#14`). Así el commit aparece en la línea de tiempo del issue.
- Mensaje claro, en presente: "Mueve", "Crea", "Corrige", "Elimina".

Si es la primera vez que haces `push` de esa rama y te pide otra cosa, Git te muestra el comando exacto; cópialo tal cual.

---

### PASO 4 – Abrir el Pull Request (el paso donde más se falla)

Hay dos caminos. Usa el que te salga más fácil.

#### Camino A: desde el banner amarillo

1. Ve a `github.com/SQEquipo3/Trapitos`.
2. Si acabas de hacer push, arriba sale un banner amarillo con tu rama y un botón **Compare & pull request**. Clic ahí.
3. **Revisa el destino** (ver checklist más abajo) y sigue con el paso 4.3.

#### Camino B: desde la pestaña Pull requests

1. Ve a `github.com/SQEquipo3/Trapitos`.
2. Arriba, clic en la pestaña **Pull requests**.
3. Botón verde **New pull request**.
4. Se abre la pantalla **Comparing changes**.

#### 4.1 Elegir bien base y compare (CRÍTICO)

Como es un fork, GitHub puede proponer por defecto el repo de origen (`Blises`). Hay que corregirlo a mano.

En la pantalla **Comparing changes** verás cuatro desplegables en una fila. Deben quedar **exactamente así**:

| Desplegable | Debe decir |
|---|---|
| **base repository** | `SQEquipo3/Trapitos` |
| **base** | `main` |
| **head repository** | `SQEquipo3/Trapitos` |
| **compare** | `tu-rama` (por ejemplo `14-integrar-main-y-utils`) |

**Si solo ves dos desplegables** (`base: main` y `compare: main`) y no ves los de repository, haz clic en el enlace **compare across forks**, justo debajo del texto "Comparing changes". Ahí aparecen los cuatro.

**Cómo cambiar cada desplegable:**

1. Clic en **base repository** → elige **`SQEquipo3/Trapitos`**.
2. Clic en **base** → elige **`main`**.
3. Clic en **head repository** → elige **`SQEquipo3/Trapitos`**.
4. Clic en **compare** → busca y elige **tu rama**.

> **Si en la pantalla dice "There isn't anything to compare"** con `base: main` y `compare: main`, es porque ambos están en `main` y son iguales. Solo falta cambiar **compare** a tu rama. También puedes hacer clic en tu rama dentro de la lista **Example comparisons**.

#### 4.2 Checklist de verificación ANTES de crear el PR

Confirma las cuatro cosas:

- [ ] La URL empieza con `github.com/SQEquipo3/Trapitos/compare/...`
- [ ] Arriba a la izquierda dice `SQEquipo3 / Trapitos` (no `Blises`)
- [ ] **base repository** = `SQEquipo3/Trapitos`
- [ ] **compare** = tu rama (no `main`)

Si alguna falla, corrígela **antes** de continuar.

#### 4.3 Crear el PR

1. Clic en el botón verde **Create pull request**.
2. **Título:** claro y con el tema, por ejemplo: `Integrar main.py y utils.py`.
3. **Descripción:** llena esto (cambia el número por el de tu issue):

   ```markdown
   ## Qué cambia
   - Crea utils.py con constantes y funciones compartidas
   - Ajusta imports en db.py, ui_contactos.py y la app

   ## Issue relacionado
   Closes #14

   ## Cómo probarlo
   1. Ejecutar `python main.py`
   2. Entrar con admin / 1234
   3. Revisar que salgan todas las pestañas
   ```

   > La línea **`Closes #14`** es la que enlaza el PR con el issue y hace que se cierre solo al mergear.

4. En la barra derecha:
   - **Assignees:** asígnate a ti.
   - **Labels:** pon la misma del issue.
   - **Projects:** selecciona **Mis Trapitos**.
   - **Reviewers:** pide revisión a un compañero.
5. Clic en **Create pull request**.

#### 4.4 Comprobar que quedó enlazado

Ya creado el PR:

1. Mira la barra derecha, sección **Development**. Debe aparecer tu issue (`#14`).
2. La URL debe ser `github.com/SQEquipo3/Trapitos/pull/NN`.
3. Ve al Project: la tarjeta debe pasar sola a **Review / QA**. Si no se movió, **arrástrala a mano**.

---

### PASO 5 – Revisión

**Quien revisa:**

1. Abre el PR.
2. Descarga la rama y pruébala:
   ```bash
   git fetch origin
   git checkout nombre-de-la-rama
   python main.py
   ```
3. Entra con `admin / 1234` y revisa que todas las pestañas funcionen.
4. En el PR, pestaña **Files changed**, revisa el código.
5. Clic en **Review changes** y elige:
   - **Approve** si todo está bien.
   - **Request changes** si hay que corregir algo (deja comentarios claros).

**Quien creó el PR**, si le piden cambios:

1. Arréglalos en tu rama (la misma, **no abras otro PR**).
2. `git add .`, `git commit -m "Corrige X (#14)"`, `git push origin tu-rama`.
3. El PR se actualiza solo.

---

### PASO 6 – Merge

Solo cuando el PR esté aprobado y **sin conflictos**:

1. En el PR, baja hasta el recuadro final.
2. Debe decir **"This branch has no conflicts with the base branch"**.
3. Clic en **Merge pull request** → **Confirm merge**.
4. Clic en **Delete branch** (botón que aparece justo después).

Resultado automático:

- El issue se cierra solo.
- La tarjeta pasa a **Done**.
- El historial queda enlazado (commits → PR → issue).

**Después del merge, TODOS actualizan su computadora:**

```bash
git checkout main
git pull origin main
```

---

### PASO 7 – Siguiente tarea

Vuelve al **Paso 1** con otro issue. **Nunca reutilices una rama anterior.**

---

## 3. Qué hacer si sale un conflicto

Un conflicto significa que dos personas cambiaron las mismas líneas. **No es un error grave.**

1. En tu rama, trae lo último de `main`:
   ```bash
   git checkout tu-rama
   git fetch origin
   git merge origin/main
   ```
2. Git te dice qué archivos tienen conflicto. Ábrelos en VS Code.
3. VS Code muestra opciones arriba de cada bloque:
   - **Accept Current Change** → te quedas con lo tuyo.
   - **Accept Incoming Change** → te quedas con lo que viene de `main`.
   - **Accept Both Changes** → dejas ambos.
4. Cuando no queden marcadores `<<<<<<<`, `=======` ni `>>>>>>>`, guarda.
5. Cierra el merge:
   ```bash
   git add archivo-que-tenia-conflicto.py
   git commit -m "Resuelve conflicto con main (#14)"
   git push origin tu-rama
   ```
6. Prueba con `python main.py` antes de mergear.

> **No borres nada "para que se quite".** Si no sabes qué opción elegir, avisa en el grupo y lo ven juntos.

**Para evitar conflictos:** antes de empezar cada tarea y cada día de trabajo, corre `git pull origin main` en tu rama. Y avisa en el grupo cuando vayas a tocar un archivo grande (`db.py`, `mis_trapitos_app_v7.py`).

---

## 4. Cómo se ve el estado en el Project

| Columna | Significa | ¿Cómo llega la tarjeta? |
|---|---|---|
| **Icebox / New Issues** | Ideas o tareas nuevas sin planear | Se crea el issue |
| **Product Backlog** | Pendiente sin sprint | Manual |
| **Sprint Backlog** | Ya está en el sprint, nadie la empieza | Manual |
| **In Progress** | Alguien la está haciendo (ya tiene rama) | **Manual** al empezar |
| **Review / QA** | Hay Pull Request abierto | Automático al enlazar el PR (o manual) |
| **Done** | PR mergeado e issue cerrado | Automático al mergear |

---

## 5. Problemas comunes y solución

| Problema | Causa | Solución |
|---|---|---|
| El PR me manda a `Blises` | Es un fork; GitHub propone el repo de origen | Cambia **base repository** a `SQEquipo3/Trapitos` |
| Dice "There isn't anything to compare" | `base` y `compare` son la misma rama (`main`) | Cambia **compare** a tu rama |
| La tarjeta no se mueve sola | El PR no está enlazado al issue | Agrega `Closes #N` en la descripción o enlázalo en **Development** |
| El issue no se cerró al mergear | Faltó `Closes #N` | Ciérralo a mano y agrega `Closes #N` en el siguiente PR |
| `git push` me rechaza | Tu rama está atrasada | `git pull origin tu-rama` y vuelve a hacer push |
| Estoy en `main` sin querer | Se me olvidó cambiar de rama | `git checkout tu-rama` (si ya hiciste cambios, avisa antes de seguir) |
| No veo mi rama en la lista de **compare** | No hiciste `push` | `git push origin tu-rama` y recarga la página |
| Sigo viendo un archivo viejo | No hiciste `pull` | `git checkout main` y `git pull origin main` |
| No sé en qué repo estoy | Se ve `Blises` arriba | Regresa a `github.com/SQEquipo3/Trapitos` |

---

## 6. Checklist final (para pegar en el grupo)

Antes de dar clic en **Create pull request**, confirma:

- [ ] El issue tiene puntos, sprint, assignee y épica
- [ ] La tarjeta estuvo en **In Progress** mientras trabajé
- [ ] Creé la rama desde el issue con source `main`
- [ ] Hice `git pull origin main` antes de abrir el PR
- [ ] Mis commits llevan `#N`
- [ ] La URL del PR empieza con `github.com/SQEquipo3/Trapitos/`
- [ ] **base repository** es `SQEquipo3/Trapitos`
- [ ] La descripción lleva `Closes #N`
- [ ] Probé con `python main.py`
- [ ] No mezclé mover archivos con cambiar lógica
- [ ] Pedí revisión a un compañero

**Resumen en una línea:**

> Issue con puntos y sprint → tarjeta a In Progress → Create a branch desde el issue → commits con `#N` → PR a **SQEquipo3/Trapitos** con `Closes #N` → revisión → merge → `git pull origin main`.
