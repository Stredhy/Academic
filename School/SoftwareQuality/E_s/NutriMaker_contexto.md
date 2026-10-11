# NutriMaker — Contexto del proyecto

> Documento de contexto recopilado a partir de la información disponible en conversaciones anteriores. Distingue los datos conocidos de los detalles que todavía no están confirmados; no pretende sustituir la documentación ni el código fuente del repositorio.

## 1. Descripción general

**NutriMaker** es un proyecto académico de software orientado a la gestión de dietas por parte de profesionales de la nutrición (nutriólogos). La aplicación permite trabajar con dietas y administrar cuentas de usuario. El usuario ha trabajado el proyecto en el contexto de una materia universitaria y de una organización de GitHub.

## 2. Tecnologías y entorno

- **Lenguaje principal:** Java.
- **Interfaz de escritorio:** JavaFX.
- **Base de datos:** MySQL/MariaDB.
- **Entorno de base de datos mencionado:** XAMPP y DBeaver.
- **Módulo Java:** `com.javafx.nutrimaker@1.0-SNAPSHOT`.
- **Control de versiones y trabajo académico:** GitHub, dentro de una organización.

No hay información suficiente en el contexto disponible para afirmar qué versión exacta de Java, JavaFX, MySQL/MariaDB, qué herramienta de construcción (Maven/Gradle) o qué estructura completa de paquetes usa el repositorio.

## 3. Funcionalidades y controladores mencionados

### 3.1 Login

- Existe un controlador de inicio de sesión denominado **Login**.
- En el contexto previo se indicó que el flujo de seguridad contempla **AES-128** y **TLS 1.2**.
- No se dispone aquí del detalle del protocolo completo, del lugar exacto donde se aplica cada mecanismo ni de una revisión del código que permita verificar su implementación.

### 3.2 Registro de usuarios

- Existe un controlador **SignUp**.
- Se mencionó una tabla/campo de cuenta de usuario con la forma `useraccount(email,password)`.
- Las contraseñas se manejan con **BCrypt**.
- Se indicó una regla de contraseña basada en la expresión regular `.{8,16}`, es decir, una longitud de entre 8 y 16 caracteres si se usa tal como está escrita. Esta expresión por sí sola no exige mayúsculas, números ni símbolos.

### 3.3 Almacenamiento y administración de dietas

Se mencionó un controlador llamado **DietStorage** con estas operaciones:

- Listar dietas.
- Crear dietas.
- Exportar dietas.
- Clonar dietas.
- Modificar dietas.
- Eliminar dietas.

### 3.4 Creación de dietas

- Existe un controlador **CreateDiet**.
- La información disponible relaciona esta parte con la creación y distribución de comidas dentro de una dieta.
- No se cuenta con suficiente contexto para describir con precisión los campos de cada alimento, cálculos nutricionales, validaciones, exportaciones o formato de archivo.

## 4. Reglas de negocio mencionadas

### 4.1 Número y nombres de comidas

Se indicó un máximo de **6 comidas**, con estos nombres:

1. `DESAYUNO`
2. `COLACION_MATUTINA`
3. `ALMUERZO`
4. `COLACION_VESPERTINA`
5. `COMIDA`
6. `CENA`

### 4.2 Distribución porcentual de comidas

Se mencionó la siguiente distribución porcentual asociada a las seis comidas:

| Comida | Porcentaje |
|---|---:|
| DESAYUNO | 25 % |
| COLACION_MATUTINA | 10 % |
| ALMUERZO | 22 % |
| COLACION_VESPERTINA | 10 % |
| COMIDA | 22 % |
| CENA | 11 % |
| **Total** | **100 %** |

Estos porcentajes suman 100 %. El contexto no especifica si representan distribución de calorías, energía, macronutrientes u otra medida; debe confirmarse en los requisitos del proyecto antes de documentarlo con mayor precisión.

## 5. Base de datos y autenticación

- La base de datos se ha trabajado usando **XAMPP**, **DBeaver** y **MariaDB/MySQL**.
- Se mencionó la tabla `useraccount` con las columnas `email` y `password`.
- Se indicó que la contraseña almacenada se protege mediante BCrypt.
- Se mencionó un archivo/clase `DatabaseClient.java` en el contexto de archivos del usuario, aunque aquí no se ha inspeccionado su contenido para determinar responsabilidades, consultas o configuración.

No se conocen con certeza el esquema completo, las claves primarias/foráneas, las tablas de dietas, alimentos o relaciones, ni las políticas de transacción y manejo de errores.

## 6. Seguridad mencionada

Los elementos de seguridad nombrados en conversaciones anteriores son:

- **BCrypt** para el tratamiento de contraseñas.
- **AES-128** y **TLS 1.2** mencionados en el contexto del inicio de sesión.
- Una validación de longitud de contraseña mediante `.{8,16}`.

Esta lista recoge lo comentado, pero no certifica que la implementación actual sea segura ni que AES-128 y TLS 1.2 estén configurados correctamente. Para una evaluación real sería necesario revisar el código, el uso de claves, certificados, conexiones y almacenamiento de credenciales.

## 7. GitHub y trabajo académico

El proyecto está asociado a una **organización de GitHub** y el usuario consultó cómo completar una actividad que pedía historias de usuario en un formato estándar. El formato solicitado fue:

```text
As a [role]
I need [function]
So that [benefit]

### Details and Assumptions
* [document what you know]

### Acceptance Criteria

Given [some context]
When [certain action is taken]
Then [the outcome of action is observed]
```

El usuario pidió que la respuesta se redactara **en español**. Una adaptación al español que conserva la estructura sería:

```text
Como [rol]
Necesito [función]
Para [beneficio]

### Detalles y supuestos
* [documentar lo que se conoce]

### Criterios de aceptación

Dado [un contexto]
Cuando [se realiza una acción]
Entonces [se observa el resultado]
```

Los criterios de aceptación se plantean en estilo **Gherkin** (`Given/When/Then`, o `Dado/Cuando/Entonces`).

### Ejemplo ilustrativo: administrar dietas

Este ejemplo se deriva de las funciones mencionadas y debe ajustarse a los requisitos oficiales del equipo:

```gherkin
Como nutriólogo
Necesito consultar las dietas que he guardado
Para encontrar y administrar una dieta existente

### Detalles y supuestos
* El usuario ha iniciado sesión.
* Existen dietas guardadas asociadas a la cuenta del usuario.

### Criterios de aceptación
Dado que el nutriólogo inició sesión
Cuando abre el apartado de almacenamiento de dietas
Entonces el sistema muestra las dietas a las que tiene acceso
```

## 8. Preferencias de trabajo y entrega conocidas

- Para actividades relacionadas con NutriMaker, el usuario pidió que el contenido estuviera **en español**.
- En trabajos académicos suele solicitar contenido que pueda adaptar o entregar en la universidad, con redacción clara y organizada.
- En el caso de las historias de usuario, la prioridad es seguir el estándar indicado por la actividad, incluyendo detalles/supuestos y criterios de aceptación en Gherkin.

## 9. Datos que no están confirmados o que faltan

No hay contexto suficiente para asegurar los siguientes puntos:

- Lista completa de requisitos funcionales y no funcionales.
- Roles exactos del sistema aparte del nutriólogo mencionado.
- Flujos detallados de login, registro, recuperación de contraseña o cierre de sesión.
- Esquema íntegro de la base de datos.
- Relaciones entre usuarios, dietas, alimentos, ingredientes y porciones.
- Cálculos nutricionales y unidades usadas.
- Detalle de exportación de dietas y formatos soportados.
- Diseño de pantallas y navegación completa.
- Arquitectura por capas, patrones de diseño y estructura completa del repositorio.
- Pruebas automatizadas, despliegue y configuración de producción.
- Estado actual de implementación de cada función.

Estos datos no deben inventarse. Si se necesita una especificación exacta, hay que contrastarlos con el repositorio, los documentos del profesor y los acuerdos del equipo.

## 10. Resumen rápido para reutilizar como contexto

NutriMaker es una aplicación académica de escritorio desarrollada en Java con JavaFX, conectada a una base de datos MariaDB/MySQL trabajada mediante XAMPP y DBeaver. Está orientada a que nutriólogos gestionen dietas. Se han mencionado los controladores `Login`, `SignUp`, `DietStorage` y `CreateDiet`. `DietStorage` incluye listar, crear, exportar, clonar, modificar y eliminar dietas. Para cuentas se mencionó `useraccount(email,password)`, contraseñas protegidas con BCrypt y una regla de longitud `.{8,16}`. En el contexto del inicio de sesión también se mencionaron AES-128 y TLS 1.2, sin detalles suficientes para verificar la implementación. Las dietas pueden organizar hasta seis comidas (`DESAYUNO`, `COLACION_MATUTINA`, `ALMUERZO`, `COLACION_VESPERTINA`, `COMIDA`, `CENA`) con porcentajes 25 %, 10 %, 22 %, 10 %, 22 % y 11 %, respectivamente. El proyecto está vinculado a una organización de GitHub y el usuario trabaja en historias de usuario en español con rol, necesidad, beneficio, detalles/supuestos y criterios de aceptación en Gherkin.
