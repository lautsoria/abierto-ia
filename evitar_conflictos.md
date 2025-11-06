# Cómo Evitar Conflictos de Merge en GitHub

Trabajar en GitHub con un equipo inevitablemente lleva a conflictos de *merge* (o conflictos de fusión), pero puedes prevenir la mayoría de ellos con un buen flujo de trabajo (workflow).

Un conflicto de merge ocurre cuando Git no puede combinar automáticamente los cambios de dos ramas diferentes. Esto suele pasar cuando dos personas editan las **mismas líneas en el mismo archivo**, o cuando una persona **elimina un archivo que otra persona modificó**.

---

### 1. Sincroniza Constantemente: Haz `pull` Antes de Hacer `push`

La causa más común de conflictos es trabajar sobre una versión desactualizada del proyecto.

* **Antes de empezar un nuevo trabajo:** Siempre trae los últimos cambios de la rama principal (ej. `main` o `develop`).
    ```bash
    # 1. Sitúate en la rama principal
    git checkout main
    
    # 2. Trae los últimos cambios
    git pull origin main
    ```
* **Antes de subir (push) tu rama:** Actualiza tu rama con cualquier cambio nuevo de `main`. Este es el paso más crítico. Usar `rebase` es una forma limpia de hacerlo.
    ```bash
    # 1. Ve a tu rama (feature branch)
    git checkout mi-rama-feature
    
    # 2. "Reaplica" tus cambios encima de la última versión de main
    git rebase main
    ```
    Si hay algún conflicto, Git se detendrá aquí y te dejará arreglarlo en tu máquina local. Una vez solucionado, puedes subir (con `git push --force-with-lease`) tu rama ya limpia.

### 2. Aísla tu Trabajo: Usa Ramas (Feature Branches)

Nunca hagas `commit` directamente a la rama `main`. Siempre crea una nueva rama para cada nueva funcionalidad (*feature*), corrección de error (*bug fix*) o tarea. Esto mantiene el código inestable separado de la base de código principal.

* **Para crear una nueva rama:**
    ```bash
    # 1. Asegúrate de empezar desde una rama 'main' actualizada
    git checkout main
    git pull origin main
    
    # 2. Crea y cámbiate a tu nueva rama
    git checkout -b mi-nueva-feature
    ```
Esto te da un entorno de pruebas (*sandbox*) dedicado. Cualquier conflicto ocurrirá cuando intentes fusionar esta rama, no en la rama principal.

### 3. Comunícate con tu Equipo

Esta es una regla no-técnica pero esencial.

* **Habla sobre lo que estás haciendo.** Si tú y un compañero están trabajando en la página de "perfil de usuario", es muy probable que toquen los mismos archivos.
* **Asigna responsables claros.** Usa tu herramienta de gestión de proyectos (como GitHub Issues) para dejar claro quién es responsable de qué parte del código.

---

### Otras Buenas Prácticas

Estos hábitos también reducirán significativamente tus probabilidades de tener conflictos.

* **Haz *commits* pequeños y frecuentes:** No trabajes durante una semana para luego intentar fusionar un `commit` gigante. Haz *commits* pequeños y lógicos (ej. "Añade validación al campo de email", "Actualiza estilo del botón"). Los *commits* pequeños son mucho más fáciles de revisar y resolver si ocurren conflictos.

* **Mantén las ramas "vivas" por poco tiempo:** Cuanto más tiempo exista tu rama, más se alejará de `main`, y mayor será la probabilidad de un conflicto masivo. Intenta fusionar (*merge*) tus ramas en uno o dos días.

* **Usa un formateador de código:** Muchos conflictos son "falsos"—son causados por diferencias en espacios en blanco, indentación (tabs vs. espacios), o puntos y coma faltantes. Usa una herramienta como **Prettier**, **ESLint**, o **Black** (para Python) para formatear automáticamente el código de todos de la misma manera al guardar.

Al seguir estos pasos, especialmente **hacer `pull`/`rebase` antes de hacer `push`** y **usar ramas para todo**, reducirás drásticamente la cantidad de conflictos de *merge* que encuentres.
