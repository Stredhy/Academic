# BankPulse MLOps --- Contexto técnico y operativo para asistentes de IA

> **Propósito de este documento:** proporcionar a otra IA el contexto
> funcional, técnico y operativo de BankPulse MLOps para que pueda
> continuar el proyecto sin inventar funcionalidades, duplicar trabajo
> ni modificar componentes delicados sin autorización.
>
> **Idioma de trabajo:** español. **Estilo de acompañamiento:**
> explicación clara, progresiva y práctica. El usuario prefiere avanzar
> paso a paso y revisar los resultados antes de continuar.

------------------------------------------------------------------------

## 1. Identidad y objetivo del proyecto

**Nombre:** BankPulse MLOps\
**Tipo:** proyecto académico de Machine Learning Operations (MLOps).\
**Problema:** clasificación binaria para estimar si un cliente
contratará un depósito bancario a plazo fijo como resultado de una
campaña de marketing telefónico.

El proyecto integra el ciclo de vida de un modelo de Machine Learning y
las herramientas de operación que exige el curso:

1.  Git y GitHub: control de versiones y colaboración.
2.  DVC: versionado de datos.
3.  MLflow: seguimiento de experimentos.
4.  Apache Airflow: orquestación de pipelines.
5.  FastAPI: API REST para predicciones y consulta del dashboard.
6.  Docker: empaquetado y ejecución de la API.
7.  GitHub Actions: integración continua y pruebas.
8.  Monitoreo: telemetría HTTP, métricas de predicciones y detección de
    Data Drift.

También se desarrolló un dashboard web propio para visualizar el estado
del ecosistema. El objetivo es que consuma datos reales de los
componentes; no se deben inventar métricas ni presentar valores
históricos estáticos como si fueran telemetría en vivo.

## 2. Reglas de colaboración con el usuario

Estas preferencias son importantes para cualquier IA que continúe el
trabajo:

-   Responder en español y mantener un tono cercano, sin sacrificar
    precisión técnica.
-   Guiar al usuario paso a paso. Evitar explicaciones excesivamente
    largas sobre etapas futuras.
-   Cuando se esté trabajando desde PowerShell, proporcionar
    **exactamente dos comandos por turno** y esperar los resultados
    antes de continuar, salvo que el usuario pida expresamente otra
    cosa.
-   Indicar siempre la rama Git actual en instrucciones que involucren
    Git o cambios del proyecto.
-   No asumir que el usuario cambió de rama. Antes de indicar
    operaciones de cambio/creación de ramas, comprobar el estado y
    explicar si debe guardar, hacer commit, push o integrar el trabajo
    actual.
-   No ordenar commits, pushes, merges, PRs, cambios de rama ni
    eliminación de recursos sin explicar primero su efecto y obtener
    autorización cuando corresponda.
-   Preferir `camelCase` en variables, funciones e identificadores
    propios. Respetar nombres existentes y convenciones obligatorias de
    herramientas.
-   El usuario prefiere que los resultados numéricos se presenten con
    **cinco decimales** cuando se trate de resultados numéricos de
    cálculos o análisis, salvo que el formato de la métrica requiera
    otra presentación.
-   No proporcionar grandes bloques de implementación si el usuario solo
    pide orientación conceptual; en el proyecto de dashboard sí se ha
    solicitado acompañamiento práctico.
-   No adelantar tecnologías o fases como si ya estuvieran implementadas
    sin comprobarlo.
-   No inventar datos, endpoints, estados de servicios, nombres de
    contenedores ni resultados de comandos.
-   El usuario quiere una solución funcional para la demostración
    académica, evitando complejidad innecesaria.

## 3. Dataset y problema de Machine Learning

Se utiliza el conjunto **Bank Marketing** del UCI Machine Learning
Repository, concretamente `bank-additional-full.csv`, guardado en el
proyecto como `data/raw/data.csv`.

  Propiedad                          Valor
  ---------------------------------- ---------------------------------------------
  Dataset                            Bank Marketing (`bank-additional-full.csv`)
  Archivo local                      `data/raw/data.csv`
  Separador                          `;`
  Filas                              41,188
  Columnas originales                21
  Variables predictoras utilizadas   20 antes de One-Hot Encoding
  Variable objetivo                  `y`
  Clases                             `no` y `yes`
  Tipo de problema                   Clasificación binaria

Distribución original conocida: - `no`: 36,548 registros. - `yes`: 4,640
registros.

El dataset contiene variables demográficas y de campaña, historial de
contactos e indicadores económicos. La variable `duration` se excluye
del conjunto de predictores porque representa la duración de la llamada
y no debe utilizarse para una predicción previa a la llamada.

Referencia académica: Moro, S., Cortez, P., & Rita, P. (2014). *A
data-driven approach to predict the success of bank telemarketing*.
Decision Support Systems, 62, 22--31.
https://doi.org/10.1016/j.dss.2014.03.001

Fuente del dataset:
https://archive.ics.uci.edu/dataset/222/bank+marketing

## 4. Procesamiento de datos

Archivo principal: `src/dataProcessing.py`.

Funciones existentes:

-   `loadData()`: carga `data/raw/data.csv` con `sep=";"`.
-   `exploreData(dataFrame)`: imprime muestras, tipos, nulos, duplicados
    y distribución de la variable objetivo.
-   `cleanData(dataFrame)`: crea `wasPreviouslyContacted` a partir de
    `pdays != 999` y reemplaza `999` en `pdays` por `NaN`. No elimina
    filas.
-   `prepareFeatures(dataFrame)`: separa `y` como objetivo, convierte
    `no` a `0` y `yes` a `1`, y elimina `y` y `duration` de las
    entradas.
-   `splitData(features, target)`: división 80/20, `random_state=42` y
    `stratify=target`.
-   `transformData(xTrain, xTest)`: detecta variables categóricas y
    numéricas; aplica imputación por mediana a numéricas y
    `OneHotEncoder(handle_unknown="ignore", sparse_output=False)` a
    categóricas. Ajusta el preprocesador solo con entrenamiento y
    transforma prueba con el mismo objeto.

Resultados de una ejecución previamente comprobada: - 41,188 filas
conservadas. - 12 duplicados detectados durante la exploración. - No se
detectaron valores nulos originales en aquella ejecución. -
`wasPreviouslyContacted`: 39,673 con valor 0 y 1,515 con valor 1. -
División: 32,950 registros de entrenamiento y 8,238 de prueba. -
Distribución de clases estratificada. - 10 columnas categóricas y 10
numéricas antes de codificar. - Matrices transformadas: entrenamiento
`(32950, 63)` y prueba `(8238, 63)`.

Los resultados anteriores son históricos de una ejecución, no deben
tratarse como mediciones en vivo.

## 5. Entrenamiento, evaluación y persistencia del modelo

Archivo: `src/modelTraining.py`.

Modelo implementado: `sklearn.linear_model.LogisticRegression` con: -
`max_iter=1000` - `class_weight="balanced"` - `solver="liblinear"` -
`random_state=42`

Flujo: 1. Cargar dataset. 2. Limpiar datos. 3. Preparar predictores y
objetivo. 4. Separar entrenamiento y prueba. 5. Ajustar y aplicar el
preprocesador. 6. Entrenar regresión logística. 7. Evaluar predicciones
y probabilidades. 8. Registrar experimento en MLflow. 9. Guardar modelo
y preprocesador.

Métricas evaluadas: - Accuracy. - ROC-AUC. - Average Precision. - Matriz
de confusión. - Reporte de clasificación.

Resultados históricos documentados en README y conversaciones: -
Accuracy: `0.834669`. - ROC-AUC: `0.801041`. - Average Precision:
`0.459830`. - Matriz de confusión de una ejecución:
`[[6277, 1033], [329, 599]]`.

No asumir que estos valores corresponden al último entrenamiento;
consultar MLflow para obtener ejecuciones actuales.

Persistencia: `src/modelPersistence.py`. -
`saveModel(model, preprocessor)` guarda `models/model.joblib` y
`models/preprocessor.joblib`. - `loadModel()` carga ambos artefactos y
genera error si no existen.

Hay una carpeta `modelsBackup/` en el snapshot del proyecto, pero el
flujo normal usa `models/`.

## 6. Versionado de datos con DVC

Configuración: `.dvc/config`.

Remote local configurado:

``` ini
[core]
    remote = localstorage
['remote "localstorage"']
    url = ../../BankPulseDvcStorage
```

Archivos DVC observados: - `data/raw/data.csv.dvc` -
`data/reference/trainingReference.csv.dvc`

El almacenamiento local se encuentra fuera del repositorio, en una
carpeta relativa `../../BankPulseDvcStorage`. Esto es importante al
mover el proyecto a otra máquina: hay que validar la existencia del
remote y no asumir que está disponible solo porque los archivos `.dvc`
estén versionados.

`api/dashboardService.py` comprueba la existencia del archivo `.dvc`
para informar si el dataset aparece rastreado. Esa comprobación no
sustituye una consulta completa al estado remoto de DVC.

## 7. Seguimiento de experimentos con MLflow

Archivo: `src/experimentTracking.py`.

-   Backend de tracking: base SQLite local `mlflow.db` en la raíz del
    proyecto.
-   Nombre del experimento: `BankPulseModelTraining`.
-   Registra parámetros del modelo y las métricas `accuracy`, `rocAuc` y
    `averagePrecision`.
-   Cada entrenamiento que llama `trackExperiment()` genera un run.

Comando documentado para entrenar desde la raíz:

``` powershell
.\.venv\Scripts\python.exe -m src.modelTraining
```

Comando documentado para la interfaz:

``` powershell
.\.venv\Scripts\mlflow.exe ui --backend-store-uri sqlite:///mlflow.db
```

UI habitual: `http://127.0.0.1:5000/`.

El dashboard lee `mlflow.db` directamente desde
`api/dashboardService.py` mediante SQLite y construye una lista de runs
con estado, fecha, métricas y parámetros. Para el dashboard, los valores
deben venir de esa base, no de una lista escrita manualmente en React.

En Windows se presentó anteriormente un bloqueo de Smart App
Control/WDAC al intentar cargar módulos binarios `.pyd` de MLflow. Se
consideró ejecutar MLflow en un entorno Linux/Docker como alternativa,
pero verificar el estado actual antes de retomar esa solución.

## 8. Orquestación con Apache Airflow

DAG: `dags/bankPulsePipeline.py`.

Configuración observada: - `dag_id`: `bankPulsePipeline`. - Zona
horaria: `America/Mexico_City`. - Programación:
`CronTriggerTimetable("0 20 1 * *", timezone=localTimezone)`. -
Ejecución programada: día 1 de cada mes a las 20:00, hora de Ciudad de
México. - `catchup=False`. - Una tarea `trainPipeline()` que ejecuta
`python -m src.modelTraining` en la ruta del proyecto montada desde
Windows en WSL.

Entorno WSL observado: - Distribución: `Ubuntu`. - Airflow instalado en
`/home/mimoe/airflowEnvironment`. -
`AIRFLOW_HOME=/home/mimoe/airflowHome`. - UI/servicio standalone en el
puerto `8080`.

### Dos scripts distintos de Airflow: no confundirlos

**A. `scripts/airflowAutoStartup.ps1`** - Script histórico para
automatización mensual. - Comprueba que se ejecute el primer día del mes
(salvo parámetro de prueba). - Inicia Airflow standalone en
Ubuntu/WSL. - Espera que Airflow y Scheduler estén saludables. - Busca
el run programado del DAG `bankPulsePipeline` de ese día a las 20:00. -
Espera hasta 180 minutos. - Si detecta que el run terminó, solicita
apagar el proceso de Airflow iniciado por el propio script. - Si falla o
expira el tiempo, deja Airflow activo para no interrumpir una ejecución
pendiente. - Escribe log en `scripts/airflowAutoStartup.log`.

**B. `scripts/bankPulseRun.ps1`** - Script de arranque integrado para el
ecosistema y el dashboard. - En el snapshot del ZIP, pretende iniciar
Docker Desktop si hace falta, levantar la API, iniciar Airflow en WSL si
está instalado, iniciar la UI de MLflow y arrancar Vite. - Abre
`http://localhost:5173/`. - Indica que `Ctrl+C` apaga los servicios que
inició. - Tiene el parámetro `-SkipDockerShutdown`. - Su bloque
`finally` detiene MLflow, detiene el contenedor API, detiene Airflow si
lo inició y, salvo que se indique lo contrario, ejecuta `wsl --shutdown`
y cierra procesos de Docker Desktop. - **Precaución importante:** el
cierre puede apagar Docker Desktop y WSL completos. No ejecutar ni
modificar este script sin revisar sus efectos y confirmar que el usuario
desea ese comportamiento. - El script puede detener procesos más amplios
que solo el dashboard. Revisar especialmente `pkill -f "airflow"` y
cierre forzado de procesos Docker antes de recomendarlo.

### Estado de la tarea programada de Windows

Se encontró una tarea programada: - Nombre: `BankPulseAirflow`. -
Ejecutable: `C:\Program Files\PowerShell\7\pwsh.exe`. - Argumento:
`-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "...BankPulseMlops\scripts\airflowAutoStartup.ps1"`. -
La tarea fue deshabilitada por el usuario mediante
`Disable-ScheduledTask -TaskName "BankPulseAirflow"`. - Confirmación
observada: `State = Disabled`.

El usuario pidió que Airflow solo se ejecute cuando el dashboard esté
activo. La tarea automática mensual debe permanecer deshabilitada salvo
que el usuario solicite lo contrario. La intención es usar un mecanismo
de arranque/parada vinculado al dashboard, pero debe revisarse y
ajustarse cuidadosamente el script integrado para que no interrumpa
ejecuciones de DAG ni apague otros servicios.

## 9. API REST con FastAPI

Directorio: `api/`.

Archivos: - `api/main.py`: instancia FastAPI, CORS, middleware de
métricas y rutas. - `api/schemas.py`: esquema de validación de entrada
del cliente. - `api/modelService.py`: carga del modelo/preprocesador y
predicción. - `api/monitoring.py`: contadores e histogramas
Prometheus. - `api/dashboardService.py`: agrega información real de
MLflow, telemetría, drift, Airflow y artefactos para el dashboard.

### Rutas principales observadas en el snapshot

  -----------------------------------------------------------------------
  Método                  Ruta                    Propósito
  ----------------------- ----------------------- -----------------------
  GET                     `/`                     Estado y versión de la
                                                  API

  GET                     `/metrics`              Métricas en formato
                                                  Prometheus; se excluye
                                                  de OpenAPI

  GET                     `/dashboard/summary`    Resumen JSON del
                                                  ecosistema para React

  POST                    `/predict`              Predicción de
                                                  contratación de
                                                  depósito
  -----------------------------------------------------------------------

`/metrics` está declarada con `include_in_schema=False`; por tanto, que
no aparezca en `/openapi.json` es intencional. Para comprobarla hay que
solicitar directamente `http://localhost:8000/metrics`.

CORS del snapshot permite: - `http://localhost:5173` -
`http://127.0.0.1:5173`

### Predicción

`api/modelService.py`: 1. Convierte el esquema Pydantic a diccionario
usando alias. 2. Construye un DataFrame de una fila. 3. Aplica
`cleanData`. 4. Ordena las características según
`preprocessor.feature_names_in_`. 5. Transforma con el preprocesador
guardado. 6. Calcula `model.predict()` y `model.predict_proba()`. 7.
Incrementa `modelPredictionsTotal` con etiqueta `prediction`. 8.
Devuelve `prediction`, `probability` y `willSubscribe`.

### Métricas Prometheus

`api/monitoring.py` declara: - `bankpulse_http_requests_total`, Counter
con etiquetas `method`, `endpoint`, `statusCode`. -
`bankpulse_http_request_duration_seconds`, Histogram con etiquetas
`method`, `endpoint`. - `bankpulse_model_predictions_total`, Counter con
etiqueta `prediction`.

El middleware de `api/main.py` registra cantidad y duración de
solicitudes HTTP, incluyendo respuestas de error. Las predicciones
incrementan el contador de clase correspondiente.

### Dashboard summary

`GET /dashboard/summary` devuelve un agregado con: - timestamp de
generación; - estado y versión de API; - contadores de solicitudes,
endpoints, predicciones por clase, total de predicciones y latencia
media; - disponibilidad e historial de MLflow; - estado de datasets y
resultados de Data Drift; - estado de conectividad de Airflow, DAG,
horario y últimas líneas del log; - presencia y tamaño de artefactos del
modelo; - detección de workflow CI.

Importante: revisar `api/dashboardService.py` para confirmar rutas,
estructura y manejo de errores antes de modificar el frontend. El
endpoint lee la base SQLite de MLflow y archivos del proyecto. En Docker
deben montarse esos archivos si se desea que el contenedor observe los
datos actuales del host.

## 10. Monitoreo y Data Drift

Archivo: `src/dataDrift.py`.

Funciones: -
`detectDataDrift(referenceData, currentData, significanceLevel=0.05)`:
compara variables numéricas comunes mediante la prueba de dos muestras
Kolmogorov--Smirnov (`ks_2samp`). -
`compareDataDrift(currentData, referencePath=None, significanceLevel=0.05)`:
carga el dataset de referencia, calcula drift y devuelve resumen.

La salida incluye: - cantidad de variables evaluadas; - cantidad de
variables con drift; - indicador global `driftDetected`; - por variable,
estadístico KS, `pValue` y `driftDetected`.

La referencia configurada por defecto es
`data/reference/trainingReference.csv`.

El servicio del dashboard compara ese dataset de referencia con
`data/raw/data.csv` después de aplicar `cleanData`. Es una comparación
del dataset local disponible, no una fuente de telemetría externa en
tiempo real. No describirla como monitoreo continuo de datos de
producción si no se ha implementado esa ingesta.

## 11. Docker

Dockerfile observado:

``` dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirementsApi.txt .

RUN pip install --no-cache-dir -r requirementsApi.txt

COPY api/ ./api/
COPY src/ ./src/
COPY models/ ./models/

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

La imagen contiene la API, código fuente, dependencias API y artefactos
del modelo. El script integrado del ZIP espera usar: - contenedor:
`bankpulseApi` - imagen: `bankpulse-api:1.2.0` - puerto: `8000:8000` -
host adicional `host.docker.internal:host-gateway` - volúmenes para
`mlflow.db`, `data/`, `scripts/` y `.github/` cuando existen.

### Diferencia entre versiones del contexto

En la conversación más reciente: - existía un contenedor llamado
`bankpulseApi` con imagen `bankpulse-api:1.0.0`; - se construyó
`bankpulse-api:1.1.0`; - se detuvo el contenedor `bankpulseApi`; - se
creó `bankpulseApiV11` con imagen `bankpulse-api:1.1.0`; - no se llegó a
confirmar que `/metrics` y `/dashboard/summary` funcionaran dentro de
ese contenedor; - luego `docker ps` falló porque Docker Desktop/Linux
engine no estaba activo.

En el ZIP suministrado: - `api/main.py` ya declara versión `1.1.0` y
ruta `/dashboard/summary`; - `scripts/bankPulseRun.ps1` está configurado
para imagen `bankpulse-api:1.2.0`; - el script elimina contenedores
legacy `bankpulseApiV11` y `bankpulseApiV12` si existen.

**No mezclar estas versiones ni ejecutar el script a ciegas.** Primero
consultar el estado actual del repositorio, Docker y los archivos
reales. El ZIP es un snapshot del repositorio y su `.git/HEAD` indica
`main`, mientras que en la conversación el usuario indicó estar
trabajando en `feat/webDashboard`. La rama actual del disco del usuario
debe comprobarse en su equipo; no asumir que el ZIP representa el estado
exacto del working tree actual.

También se observó que Docker Desktop no estaba ejecutándose en el
último diagnóstico: - `wsl --list --verbose` mostró
`docker-desktop Stopped` y `Ubuntu Stopped`. -
`Get-Process "Docker Desktop", "com.docker.backend"` no devolvió
procesos. - `docker ps` falló al conectar con
`npipe:////./pipe/dockerDesktopLinuxEngine`.

Esto no demuestra que se hayan perdido imágenes o contenedores; solo que
el motor Docker no estaba disponible en ese momento.

## 12. GitHub Actions / CI

Workflow: `.github/workflows/ci.yml`.

Nombre: `BankPulse CI`.

Disparadores observados: - push a `main` y `feat/githubActions`; - pull
request dirigido a `main`.

Job: 1. Checkout. 2. Configura Python 3.13. 3. Instala
`requirements.txt`. 4. Prepara dataset mediante
`scripts.ci.prepareCiData`. 5. Prepara modelo mediante
`scripts.ci.prepareCiModel`. 6. Ejecuta `python -m pytest tests/ -v`. 7.
Construye imagen Docker `bankpulse-api:ci`.

No afirmar que se ejecuta en todas las ramas: el YAML observado limita
los eventos de push a las ramas indicadas y PR hacia `main`.

## 13. Dashboard web

Directorio: `frontend/`.

Tecnologías observadas en `package.json`: - React 19. - TypeScript. -
Vite 8. - Tailwind CSS 4 con `@tailwindcss/vite`. - Lucide React. -
Recharts. - Oxlint.

Comandos habituales desde `frontend/`:

``` powershell
npm install
npm run dev
npm run build
npm run lint
```

Servidor local de desarrollo: `http://localhost:5173/`.

La interfaz utiliza una estética oscura con paleta vino/borgoña, fondos
casi negros, bordes y acentos rosa/vino. El usuario quiere un dashboard
visualmente cuidado, moderno y coherente; no sacrificar legibilidad por
decoración.

En el snapshot del ZIP: - `frontend/src/App.tsx` solicita
`GET http://localhost:8000/dashboard/summary`. - Refresca los datos cada
15 segundos. - Presenta estados de carga y error. - No pretende mostrar
métricas simuladas cuando FastAPI no responde. - El sidebar muestra
estado de conexión de API y Airflow. - Las secciones incluyen resumen,
experimentos y monitoreo, entre otras. - La vista principal usa datos de
la respuesta `DashboardSummary`. - `frontend/vite.config.ts` configura
React y Tailwind, sin proxy de API; el frontend usa URL absoluta
`http://localhost:8000`. - El dashboard representa datos de MLflow,
Prometheus, DVC/Data Drift, Airflow, artefactos y CI.

En una conversación previa, el frontend estaba en una etapa más temprana
con `Sidebar.tsx`, `MetricCard.tsx`, `Dashboard.tsx` y
`ModelPerformanceChart.tsx` que mostraban algunos valores históricos
escritos en el código. El usuario cuestionó explícitamente si los datos
eran reales y exigió que todo fuera dinámico. El ZIP parece contener una
evolución posterior que ya consume `/dashboard/summary`; verificar
archivos actuales antes de concluir cuál versión está en el working
tree.

**Regla de producto:** mostrar `—`, "Sin datos", "Desconectado" o
mensajes de error cuando un componente no esté disponible. Nunca
reemplazar una fuente desconectada por números inventados.

## 14. Script integrado para arrancar el ecosistema

Archivo observado en el ZIP: `scripts/bankPulseRun.ps1`.

Objetivo aparente: iniciar Docker Desktop, API, Airflow, MLflow UI y
Vite; abrir el dashboard; al pulsar `Ctrl+C`, cerrar servicios
iniciados.

Advertencias antes de utilizarlo: - Su imagen configurada es
`bankpulse-api:1.2.0`, no la `1.1.0` creada en el flujo reciente. -
Puede eliminar contenedores llamados `bankpulseApiV11` y
`bankpulseApiV12`. - Puede eliminar/recrear `bankpulseApi` si detecta
una imagen distinta. - Puede iniciar Airflow en WSL. - Al cerrar puede
ejecutar `wsl --shutdown` y cerrar procesos de Docker Desktop. - El
bloque de apagado de Airflow utiliza `pkill -f "airflow"`, que puede
afectar procesos de Airflow ajenos al dashboard. - `-SkipDockerShutdown`
evita el cierre global de Docker/WSL, pero el script sigue deteniendo el
contenedor de API y Airflow que haya iniciado. - Debe revisarse antes de
confiarle la administración completa de los servicios.

El usuario desea que Airflow se ejecute solamente cuando el dashboard
esté activo. La tarea programada mensual `BankPulseAirflow` está
deshabilitada. La solución debe respetar esa decisión y no reactivar la
tarea automáticamente.

## 15. Estructura del repositorio observada

Estructura principal (omitiendo dependencias, cachés, entornos virtuales
y archivos generados):

``` text
BankPulseMlops/
├── .dvc/
│   └── config
├── .github/
│   └── workflows/
│       └── ci.yml
├── api/
│   ├── dashboardService.py
│   ├── main.py
│   ├── modelService.py
│   ├── monitoring.py
│   └── schemas.py
├── dags/
│   └── bankPulsePipeline.py
├── data/
│   ├── raw/
│   │   ├── data.csv
│   │   └── data.csv.dvc
│   └── reference/
│       ├── trainingReference.csv
│       └── trainingReference.csv.dvc
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.ts
├── models/
│   ├── model.joblib
│   └── preprocessor.joblib
├── modelsBackup/
├── scripts/
│   ├── airflowAutoStartup.ps1
│   ├── bankPulseRun.ps1
│   ├── bankPulseRun.sh
│   └── ci/
├── src/
│   ├── dataDrift.py
│   ├── dataProcessing.py
│   ├── experimentTracking.py
│   ├── modelPersistence.py
│   └── modelTraining.py
├── tests/
├── Dockerfile
├── mlflow.db
├── requirements.txt
├── requirementsApi.txt
└── README.md
```

## 16. Pruebas

En el historial del proyecto se reportaron 31 pruebas automatizadas
aprobadas. El ZIP incluye pruebas para: - procesamiento de datos; -
entrenamiento; - persistencia; - tracking de experimentos; - FastAPI; -
monitoreo; - Data Drift.

No afirmar que siguen pasando en el estado actual sin ejecutar la suite
en el entorno del usuario.

Comando habitual:

``` powershell
python -m pytest tests/ -v
```

## 17. Estado operativo conocido al momento de redactar este contexto

### Proyecto / Git

-   Ruta Windows habitual:
    `C:\Users\mimoe\OneDrive\Documentos\ProyectDataMining\BankPulseMlops`
-   En la conversación reciente, el prompt mostraba la rama
    `feat/webDashboard`.
-   El ZIP analizado trae `.git/HEAD` apuntando a `main`. Por tanto,
    verificar la rama real local antes de dar instrucciones Git.
-   Hay cambios locales del frontend en el historial de conversación; no
    asumir working tree limpio.

### Dashboard

-   Vite se había iniciado correctamente en el pasado en
    `http://localhost:5173/`.
-   El usuario detuvo el servidor local y luego no pudo volver a ver la
    interfaz.
-   La forma básica de volver a mostrarlo es entrar a `frontend/` y
    ejecutar `npm run dev`, siempre que las dependencias estén
    instaladas.
-   Detener Vite no borra los archivos del dashboard; solo detiene el
    servidor de desarrollo.
-   React depende de FastAPI en `http://localhost:8000` para poblar el
    resumen. Si FastAPI está apagada, la interfaz puede cargar pero
    mostrará un estado de desconexión/error.

### API / Docker

-   Se construyó `bankpulse-api:1.1.0`.
-   Se detuvo el contenedor `bankpulseApi` que usaba
    `bankpulse-api:1.0.0`.
-   Se creó `bankpulseApiV11` con la imagen `bankpulse-api:1.1.0`.
-   No se confirmó el funcionamiento de `/metrics` ni de
    `/dashboard/summary` dentro de ese contenedor.
-   Posteriormente Docker Desktop no estaba activo y `docker ps` falló
    al conectar con el engine.
-   No eliminar imágenes ni contenedores sin comprobar el estado actual.

### Airflow / WSL

-   `Ubuntu` y `docker-desktop` aparecían detenidos en WSL.
-   La tarea programada `BankPulseAirflow` quedó en estado `Disabled`.
-   No reactivar esa tarea sin petición explícita.
-   El script `airflowAutoStartup.ps1` es la automatización mensual
    antigua, no debe usarse como script de arranque del dashboard.
-   El script `bankPulseRun.ps1` del ZIP contiene un intento de
    orquestar el ecosistema, pero necesita revisión antes de ejecutarse
    por sus efectos de apagado global y sus nombres/versiones de
    contenedor.

### MLflow

-   `mlflow.db` existe en el snapshot del ZIP.
-   MLflow UI normalmente usa el puerto `5000`.
-   Comprobar compatibilidad y disponibilidad del entorno antes de
    iniciar.

## 18. Próximas prioridades recomendadas

Orden de trabajo prudente:

1.  **Recuperar y verificar el dashboard local:** comprobar archivos
    actuales, instalar dependencias si hace falta y arrancar Vite.
    Confirmar que la interfaz carga.
2.  **Verificar la rama y estado del repositorio:** no cambiar de rama
    ni descartar cambios.
3.  **Revisar el launcher `scripts/bankPulseRun.ps1`:** alinear imagen
    Docker con la versión real; evitar borrar contenedores
    inesperadamente; evitar apagar Docker/WSL globalmente; detener solo
    procesos que el propio launcher haya iniciado; no matar una
    ejecución Airflow activa.
4.  **Arrancar Docker Desktop manualmente o desde un launcher seguro**,
    esperar a que el engine responda y listar contenedores/imágenes.
5.  **Verificar la API actual:** probar `/`, `/metrics`,
    `/dashboard/summary` y `/docs`; probar `/predict` con un payload
    válido.
6.  **Confirmar la conexión React → FastAPI:** el dashboard debe
    refrescar datos reales y reflejar correctamente estados
    desconectados.
7.  **Validar datos del dashboard:** contrastar métricas de MLflow,
    Prometheus, Data Drift, artefactos y Airflow con sus fuentes.
8.  **Implementar inicio/parada coordinado** para React, FastAPI,
    Airflow y MLflow solo después de conocer qué servicios ya estaban
    activos antes del lanzamiento. No detener servicios que el launcher
    no inició.
9.  **Ejecutar pruebas y build del frontend** después de los cambios.
10. **Documentar y preparar la demostración académica** cuando el
    sistema esté estable.

## 19. Instrucciones esenciales para la IA que reciba este archivo

Antes de proponer cambios: - Preguntar o comprobar qué archivos y
servicios están realmente activos. - Diferenciar el snapshot del ZIP del
estado vivo del equipo. - No asumir que la API Docker `1.1.0` es la
última: el launcher del ZIP apunta a `1.2.0`, y el estado actual debe
verificarse. - No confundir la tarea programada `BankPulseAirflow` con
el servicio Airflow en WSL. - No volver a habilitar el inicio automático
mensual de Airflow sin permiso. - No asumir que `localhost:5173` y
`localhost:8000` siguen activos porque hayan funcionado antes. - No
hardcodear datos de MLflow, Prometheus, DVC, Airflow o métricas de
modelo en el frontend. - Si una fuente está caída, mostrar su
indisponibilidad claramente. - No borrar contenedores, imágenes,
volúmenes, bases de datos, artefactos ni archivos del usuario sin
autorización. - Para comandos de PowerShell, respetar el flujo de dos
comandos por turno y esperar la salida.

**Meta final:** un dashboard web BankPulse de estética vino/borgoña, con
datos reales del ecosistema MLOps, y un mecanismo confiable para iniciar
y detener los servicios vinculados al dashboard sin automatizaciones
inesperadas ni apagados colaterales.
