# NutriMaker con MySQL

AplicaciÃ³n de escritorio JavaFX para registrar usuarios, pacientes y dietas. Ahora se conecta directamente a MySQL mediante JDBC (MySQL Connector/J 9.7.0).

## QuÃ© se cambiÃ³ y por quÃ©

La versiÃ³n recibida no tenÃ­a una conexiÃ³n JDBC a Oracle: los repositorios enviaban peticiones HTTP a servicios ORDS de Oracle Cloud. Cambiar solamente una URL no permitÃ­a usar MySQL.

- Se sustituyeron las llamadas REST por consultas SQL parametrizadas en los repositorios de usuarios, pacientes, comidas y dietas.
- Se aÃ±adiÃ³ el esquema MySQL en `database/mysql/01_schema.sql`, con claves forÃ¡neas, Ã­ndices e identificadores `AUTO_INCREMENT`.
- Las credenciales se leen de variables de entorno. Las contraseÃ±as de los usuarios de la aplicaciÃ³n siguen almacenÃ¡ndose como hashes BCrypt.
- El paciente creado pasa su ID al formulario de dieta. Las dietas usan el ID devuelto por su propia inserciÃ³n; ya no se consulta el Ãºltimo registro global.
- Crear y clonar una dieta usa una transacciÃ³n. Si falla una inserciÃ³n, se revierte la operaciÃ³n.
- El contador de dietas se filtra por usuario, igual que el listado paginado.
- Al recuperar una dieta, las comidas se agrupan por cada registro programado; repetir un alimento en distintos dÃ­as ya no elimina esas repeticiones.

**Alcance:** no se proporcionÃ³ el DDL ni una exportaciÃ³n de Oracle. El esquema se reconstruyÃ³ a partir del cÃ³digo y no representa una copia verificada del esquema remoto. No se modificÃ³ Oracle ni se trasladaron sus registros. El catÃ¡logo incluido es ficticio y opcional.

## 1. Requisitos

- MySQL Server 8.0.16 o superior; los scripts estÃ¡n orientados a MySQL 8.x, incluido 8.4.
- MySQL Workbench o el cliente de consola `mysql`. Workbench es un cliente: necesitas tambiÃ©n un servidor.
- JDK 23 o posterior; el proyecto conserva JavaFX 23.0.1 y compila para Java 23.
- Acceso a Internet la primera vez para que Maven descargue las dependencias.

Configura `JAVA_HOME` con la carpeta de tu JDK. Maven estÃ¡ incluido mediante `mvnw.cmd`.

En el equipo revisado habÃ­a MariaDB 12.3, no una instalaciÃ³n identificada de MySQL Server. Si instalas MySQL junto a MariaDB, usa un puerto libre y ajusta la URL del paso 3.

## 2. Crear la base de datos

### Desde MySQL Workbench

1. ConÃ©ctate a tu servidor con un usuario administrador.
2. Abre `database/mysql/01_schema.sql` en **File > Open SQL Script** y ejecuta todo el archivo.
3. Si quieres probar el programa sin importar todavÃ­a tu catÃ¡logo, abre y ejecuta `database/mysql/02_demo_data.sql` **una sola vez**.
4. Actualiza **Schemas**. Debe aparecer `nutrimaker` con siete tablas.
5. Ejecuta el siguiente SQL, sustituyendo la contraseÃ±a de ejemplo por una propia:

```sql
CREATE USER 'nutrimaker'@'localhost' IDENTIFIED BY 'CAMBIA_ESTA_CLAVE';
GRANT SELECT, INSERT, UPDATE, DELETE ON nutrimaker.* TO 'nutrimaker'@'localhost';
```

Si ese usuario ya existe, utiliza sus credenciales o cambia su contraseÃ±a conscientemente con `ALTER USER`. La cuenta MySQL `nutrimaker` conecta Java a la base de datos; las cuentas registradas en la ventana de NutriMaker se guardan en `useraccount` y son independientes.

### Alternativa: consola MySQL

Desde PowerShell:

```powershell
mysql -u root -p
```

Ya dentro del cliente MySQL:

```sql
SOURCE C:/Users/jaret/Downloads/NutriMaker_v1-main/database/mysql/01_schema.sql;
SOURCE C:/Users/jaret/Downloads/NutriMaker_v1-main/database/mysql/02_demo_data.sql;
CREATE USER 'nutrimaker'@'localhost' IDENTIFIED BY 'CAMBIA_ESTA_CLAVE';
GRANT SELECT, INSERT, UPDATE, DELETE ON nutrimaker.* TO 'nutrimaker'@'localhost';
EXIT;
```

Ajusta la ruta si mueves el proyecto. El primer script no elimina tablas existentes, pero `IF NOT EXISTS` tampoco actualiza una tabla incompatible: Ãºsalo en una base nueva.

## 3. Configurar y ejecutar NutriMaker

Abre PowerShell en la carpeta del proyecto. Sustituye la contraseÃ±a por la que asignaste en MySQL:

```powershell
cd C:\Users\jaret\Downloads\NutriMaker_v1-main
$env:NUTRIMAKER_DB_URL = 'jdbc:mysql://localhost:3306/nutrimaker?connectionTimeZone=UTC&forceConnectionTimeZoneToSession=true'
$env:NUTRIMAKER_DB_USER = 'nutrimaker'
$env:NUTRIMAKER_DB_PASSWORD = 'CAMBIA_ESTA_CLAVE'
.\mvnw.cmd clean javafx:run
```

Estas variables duran solamente en esa terminal y sus procesos. Si ejecutas desde IntelliJ o NetBeans, aÃ±Ã¡delas a las variables de entorno de la configuraciÃ³n de ejecuciÃ³n. No se carga automÃ¡ticamente un archivo `.env`.

Los valores predeterminados son servidor `localhost`, puerto `3306`, base `nutrimaker` y usuario `nutrimaker`; la contraseÃ±a es obligatoria. Las fechas de creaciÃ³n usan UTC; las fechas y horas de las comidas conservan el calendario programado.

En la aplicaciÃ³n:

1. Registra una cuenta e inicia sesiÃ³n.
2. Crea un paciente.
3. Crea una dieta, por ejemplo de 1500 calorÃ­as, tres comidas y domingo de descanso.
4. Consulta el listado, clona una dieta o elimÃ­nala.

El catÃ¡logo debe contener alimentos de tipo `BREAKFAST`, `LUNCH`, `DINNER` y, si eliges cuatro a seis comidas, `SNACK`. Si no cabe ningÃºn alimento en el presupuesto de un horario, la aplicaciÃ³n no guarda la dieta. El algoritmo existente aproxima el objetivo con los alimentos disponibles; no garantiza alcanzar exactamente las calorÃ­as indicadas.

## 4. Consultar y cargar datos desde MySQL

Puedes abrir `database/mysql/03_check.sql` en Workbench o ejecutar:

```sql
USE nutrimaker;
SHOW TABLES;
SELECT user_id, email FROM useraccount;
SELECT * FROM patient;

SELECT d.diet_id, p.name AS paciente, d.creation_date, d.calories
FROM diet d
JOIN patient p ON p.patient_id = d.patient_id
ORDER BY d.diet_id DESC;

SELECT dm.day, dm.time_of_day, dm.meal_type, m.name
FROM diet_meal dm
JOIN mealbase m ON m.meal_base_id = dm.meal_base_id
WHERE dm.diet_id = 1
ORDER BY dm.day, dm.time_of_day;
```

Sustituye `1` por un ID real. Las tablas se relacionan asÃ­:

| Tabla | Contenido |
|---|---|
| `useraccount` | Correo y hash BCrypt de cada cuenta |
| `patient` | Nombre, edad, peso y altura |
| `mealbase` | CatÃ¡logo de alimentos/comidas y valores nutricionales |
| `ingredient` | Nombres de ingredientes |
| `meal_ingredient` | Ingredientes, cantidades y unidades de cada comida |
| `diet` | Usuario, paciente, totales y configuraciÃ³n de la dieta |
| `diet_meal` | Comida, fecha y hora programadas en cada dieta |

Para aÃ±adir una comida, usa `INSERT INTO mealbase (...)` con sus valores reales. Los nombres exactos de columnas estÃ¡n en el esquema; `meal_type` usa los cÃ³digos en inglÃ©s anteriores. Las calorÃ­as deben ser como mÃ­nimo 1. Inserta despuÃ©s sus ingredientes y relaciones si quieres que aparezcan en el detalle.

Eliminar una dieta elimina sus registros de `diet_meal` automÃ¡ticamente. Los pacientes y alimentos referenciados no se pueden borrar hasta resolver sus relaciones.

## 5. Si quieres conservar los datos de Oracle

Hace falta una exportaciÃ³n autorizada de las tablas originales (por ejemplo CSV) y sus definiciones. No basta con importar SQL de Oracle directamente en MySQL.

1. Compara las columnas originales con este esquema y adapta el mapeo.
2. Importa primero usuarios, pacientes, catÃ¡logo e ingredientes, luego dietas y finalmente las tablas de relaciones.
3. Conserva los ID originales para mantener las referencias. MySQL puede aceptar ID explÃ­citos en columnas `AUTO_INCREMENT`.
4. Conserva los hashes BCrypt existentes; no insertes contraseÃ±as en texto plano ni vuelvas a aplicar un hash al hash.
5. Convierte las fechas Oracle/ISO a `YYYY-MM-DD` para `day` y a `YYYY-MM-DD HH:MM:SS` para `DATETIME`, usando UTC para fechas de creaciÃ³n.
6. Compara recuentos y relaciones antes de usar la aplicaciÃ³n con esos datos.

No combines sin revisar los datos ficticios con una importaciÃ³n que reutilice sus ID.

## 6. Problemas frecuentes

| Mensaje o sÃ­ntoma | QuÃ© revisar |
|---|---|
| `Define NUTRIMAKER_DB_PASSWORD` | Configura la variable en el proceso que inicia Java |
| `Access denied` | Usuario, contraseÃ±a, host autorizado y permisos MySQL |
| `Communications link failure` | Servicio iniciado, host y puerto de la URL |
| `Unknown database` o tabla inexistente | Ejecuta `01_schema.sql` en el servidor correcto |
| `Public Key Retrieval is not allowed` | Configura TLS o la clave pÃºblica del servidor; para desarrollo exclusivamente local puedes aÃ±adir `&allowPublicKeyRetrieval=true` a la URL |
| `invalid target release: 23` | Maven estÃ¡ usando un JDK anterior a 23 |
| No se crea una dieta | Revisa el catÃ¡logo, los tipos y las calorÃ­as mÃ­nimas; consulta el error en la terminal |
| El registro dice que el correo existe | La interfaz heredada tambiÃ©n muestra ese mensaje ante fallos de conexiÃ³n; consulta la terminal |

## 7. VerificaciÃ³n y pruebas

Se compilÃ³ el proyecto con JDK 25, conservando el destino Java 23, y MySQL Connector/J 9.7.0. Pasaron dos pruebas de integraciÃ³n (cero fallos) contra una instancia **temporal de MariaDB 12.3.2**: registro/login BCrypt, consultas parametrizadas, pacientes, generaciÃ³n de dieta, comidas repetidas, ingredientes, paginaciÃ³n por usuario, clonaciÃ³n, actualizaciÃ³n, borrado en cascada y rollback. Los scripts de esquema y catÃ¡logo se ejecutaron correctamente en esa instancia.

**Pendiente de comprobar en tu instalaciÃ³n:** ejecuciÃ³n contra MySQL Server y recorrido visual completo de JavaFX. No se probÃ³ ni importÃ³ el servidor remoto de Oracle.

Las pruebas estÃ¡n en `src/test/java/com/javafx/nutrimaker/repository/MySqlMigrationTest.java`. Por defecto se omiten para no escribir en tu base habitual. Para repetirlas, prepara una base independiente con el esquema y el catÃ¡logo demo, configura las variables del paso 3 para esa base y ejecuta:

```powershell
$env:NUTRIMAKER_RUN_DB_TESTS = 'true'
.\mvnw.cmd test
Remove-Item Env:NUTRIMAKER_RUN_DB_TESTS
```

Las pruebas crean registros con identificadores propios y los eliminan al terminar. Usa siempre una base de pruebas.

Referencias oficiales: [Connector/J con Maven](https://dev.mysql.com/doc/connector-j/en/connector-j-installing-maven.html) y [sintaxis de la URL JDBC](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-jdbc-url-format.html).
