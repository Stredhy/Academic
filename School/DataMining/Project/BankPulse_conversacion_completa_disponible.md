# Conversación --- BankPulse MLOps y dashboard web

> **Nota sobre el alcance:** este documento reúne la conversación
> disponible en el contexto actual. La parte anterior del desarrollo del
> dashboard llegó a esta conversación como un resumen de continuidad, no
> como una transcripción literal completa. Por eso se incluye una
> síntesis de ese contexto y, después, la transcripción íntegra de los
> mensajes disponibles en este tramo.

## 1. Contexto previo del proyecto

El proyecto académico **BankPulse MLOps** está ubicado en:

`C:\Users\mimoe\OneDrive\Documentos\ProyectDataMining\BankPulseMlops`

La rama de trabajo actual es `feat/webDashboard`.

El objetivo es construir un dashboard web personalizado en tonos
vino/burdeos, con modo oscuro, usando:

-   React
-   TypeScript
-   Tailwind CSS
-   Vite
-   Lucide React
-   Recharts

El dashboard debe consumir datos reales y dinámicos del proyecto, no
inventar métricas ni presentar datos simulados como si fueran actuales.

El proyecto integra componentes MLOps como Git/GitHub, DVC, MLflow,
Airflow, FastAPI, Docker, GitHub Actions y monitoreo.

### Estado conocido del frontend

-   El frontend se creó con Vite y React + TypeScript.
-   Tailwind CSS y Lucide React están instalados.
-   Se creó un componente `Sidebar.tsx` con navegación.
-   Se creó `MetricCard.tsx` para tarjetas de métricas.
-   Se creó `Dashboard.tsx` con métricas históricas que inicialmente
    estaban escritas de forma estática.
-   Se creó `ModelPerformanceChart.tsx` con Recharts.
-   `App.tsx` integra el menú lateral, el dashboard y la gráfica.
-   El servidor de desarrollo de Vite se utiliza en
    `http://localhost:5173/`.
-   El usuario quiere que los datos pasen a consultarse dinámicamente
    desde FastAPI, MLflow, Airflow, DVC, monitoreo y CI/CD, mostrando
    estados sin datos o servicios desconectados cuando corresponda.

### Estado conocido del backend

FastAPI se ejecuta en el puerto `8000`. El código de `api/main.py`
incluye middleware de monitoreo, la ruta `/`, la ruta `/metrics` (oculta
del esquema OpenAPI con `include_in_schema=False`) y la ruta POST
`/predict`.

El archivo `api/monitoring.py` define:

-   `httpRequestsTotal`
-   `httpRequestDurationSeconds`
-   `modelPredictionsTotal`

En `api/modelService.py`, cada predicción incrementa
`modelPredictionsTotal` con la etiqueta `prediction`.

La imagen Docker original era `bankpulse-api:1.0.0`, con un contenedor
llamado `bankpulseApi`. Se construyó posteriormente
`bankpulse-api:1.1.0` para incorporar el código actualizado.

### Preferencias de trabajo

-   Conversación en español y tono cercano.
-   Trabajar paso a paso.
-   Dar exactamente dos comandos por turno cuando se está guiando con
    PowerShell y esperar los resultados.
-   Indicar la rama actual: `feat/webDashboard`.
-   No asumir que se ha cambiado de rama.
-   No realizar cambios destructivos sin comprobar antes el estado.
-   Usar camelCase en nombres propios del código cuando sea posible.
-   No presentar métricas estáticas como datos dinámicos o actuales.

------------------------------------------------------------------------

## 2. Transcripción disponible

### Usuario

``` text
  ~/.../Documentos/ProyectDataMining/BankPulseMlops  feat/webDashboard ≢  ?1  1ms   
14:36:55
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/metrics" -ErrorAction Stop
    Write-Host "HTTP:" $response.StatusCode
    ($response.Content -split "`n" | Select-String "bankpulse_" | Select-Object -First 15).Line
} catch {
    Write-Host "No se pudo consultar /metrics:" $_.Exception.Message
}
No se pudo consultar /metrics: El código de estado de la respuesta no indica un resultado correcto: 404 (Not Found).

14:37:28
Get-Content api/modelService.py
import pandas as pd

from api.schemas import ClientData
from src.dataProcessing import cleanData
from src.modelPersistence import loadModel
from api.monitoring import modelPredictionsTotal


model, preprocessor = loadModel()


def predictClient(clientData: ClientData):
    # Recuperar los nombres originales del dataset
    clientDictionary = clientData.model_dump(by_alias=True)

    # Convertir la solicitud en una fila de datos
    dataFrame = pd.DataFrame([clientDictionary])

    # Aplicar la misma limpieza utilizada en entrenamiento
    cleanedData = cleanData(dataFrame)

    # Respetar el orden de las características del modelo
    features = cleanedData[
        list(preprocessor.feature_names_in_)
    ]

    # Aplicar el preprocesador entrenado
    transformedFeatures = preprocessor.transform(features)

    # Generar clasificación y probabilidad de contratación
    prediction = int(model.predict(transformedFeatures)[0])
    probability = float(
        model.predict_proba(transformedFeatures)[0, 1]
    )

    modelPredictionsTotal.labels(
        prediction=str(prediction)
    ).inc()

    return {
        "prediction": prediction,
        "probability": probability,
        "willSubscribe": bool(prediction)
    }
```

### Asistente

¡Ya encontramos el problema, mi cabronzote! Y afortunadamente no es un
error de nuestro código de monitoreo.

El endpoint `/metrics` devuelve HTTP 404. Esto significa que el servidor
que responde en `localhost:8000` no reconoce esa ruta.

El contador de predicciones está implementado correctamente en
`api/modelService.py`; cada predicción incrementa el contador
correspondiente a la clase `0` o `1`.

Se solicitó ejecutar:

``` powershell
docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
```

y:

``` powershell
Get-Content Dockerfile
```

### Usuario

``` text
14:38:09
docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
NAMES               IMAGE                             STATUS                   PORTS
bankpulseApi        bankpulse-api:1.0.0               Up 52 minutes            0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
welcome-to-docker   docker/welcome-to-docker:latest   Exited (0) 3 weeks ago

14:38:10
Get-Content Dockerfile
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

### Asistente

Se explicó que el contenedor `bankpulseApi` estaba ejecutando
`bankpulse-api:1.0.0`, y se propuso construir una imagen actualizada
`1.1.0` sin modificar el Dockerfile.

Comandos propuestos:

``` powershell
docker build -t bankpulse-api:1.1.0 .
```

``` powershell
docker images bankpulse-api
```

### Usuario

``` text
14:38:39
docker build -t bankpulse-api:1.1.0 .
[+] Building 152.8s (13/13) FINISHED
...
=> naming to docker.io/library/bankpulse-api:1.1.0
...

14:41:13
docker images bankpulse-api
IMAGE                 ID             DISK USAGE   CONTENT SIZE   EXTRA
bankpulse-api:1.0.0   008b6876c0b9        683MB          156MB    U
bankpulse-api:1.1.0   952f222f23a4        684MB          157MB
```

### Asistente

Se explicó que la imagen anterior se conservaba como respaldo y que solo
había un contenedor ejecutándose. Se propuso detener el contenedor
anterior e iniciar uno nuevo con la imagen `1.1.0`.

``` powershell
docker stop bankpulseApi
```

``` powershell
docker run -d --name bankpulseApiV11 -p 8000:8000 bankpulse-api:1.1.0
```

### Usuario

``` text
14:41:25
docker stop bankpulseApi
bankpulseApi

14:42:02
docker run -d --name bankpulseApiV11 -p 8000:8000 bankpulse-api:1.1.0
e4e90cce6b8c72c7043d82b1b14442becbf3e0ad8100ad25ebc5cbdddbc54e48
```

### Asistente

Se indicó comprobar la ruta raíz y el endpoint de métricas:

``` powershell
Invoke-RestMethod -Uri "http://localhost:8000/"
```

``` powershell
$response = Invoke-WebRequest -Uri "http://localhost:8000/metrics"; Write-Host "HTTP:" $response.StatusCode; ($response.Content -split "`n" | Select-String "bankpulse_" | Select-Object -First 20).Line
```

### Usuario

``` text
Que hace ahi el bankPulseAirflow?
```

### Asistente

Se explicó que Apache Airflow es el componente encargado de orquestar
procesos del proyecto mediante DAGs. Se aclaró que `bankPulseAirflow` no
aparecía en la lista de contenedores que se había compartido, por lo que
se pidió comprobar si era una tarea programada de Windows.

### Usuario

``` text
Que hace ahi el bankPulseAirflow? [salida de PowerShell]

Get-ScheduledTask | Where-Object {
    $_.Actions.Execute -match 'powershell|pwsh|cmd|wscript|cscript|\.bat|\.ps1|\.vbs'
} | Select-Object TaskName, TaskPath, State, Actions | Format-List

TaskName : BankPulseAirflow
TaskPath : \
State    : Ready
Actions  : {MSFT_TaskExecAction}

TaskName : EnergySettings
TaskPath : \
State    : Ready
Actions  : {MSFT_TaskExecAction}

...
```

### Asistente

Se explicó que `BankPulseAirflow` era una tarea programada de Windows,
posiblemente creada para iniciar Airflow. Se solicitaron los detalles de
la acción y los activadores.

### Usuario

``` text
PowerShell 7.6.10
La carga de perfiles personales y del sistema tardó 2017ms.

Get-ChildItem "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"

Directorio: C:\Users\mimoe\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

Name
----
desktops.ahk - Acceso directo.lnk
Enviar a OneNote.lnk

Get-ScheduledTask | Where-Object {
    $_.Actions.Execute -match 'powershell|pwsh|cmd|wscript|cscript|\.bat|\.ps1|\.vbs'
} | Select-Object TaskName, TaskPath, State, Actions | Format-List

TaskName : BankPulseAirflow
TaskPath : \
State    : Ready
Actions  : {MSFT_TaskExecAction}

...

(Get-ScheduledTask -TaskName "BankPulseAirflow").Actions | Format-List *

Id                    :
Arguments             : -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "C:\Users\mimoe\OneDrive\Documentos\ProyectDataMining\BankPulseMlops\scripts\airflowAutoStartup.ps1"
Execute               : C:\Program Files\PowerShell\7\pwsh.exe
WorkingDirectory      :

(Get-ScheduledTask -TaskName "BankPulseAirflow").Triggers | Format-List *

Enabled               : True
StartBoundary         : 2026-11-10T19:55:00
...
```

### Asistente

Se identificó que la tarea ejecutaba:

`C:\Users\mimoe\OneDrive\Documentos\ProyectDataMining\BankPulseMlops\scripts\airflowAutoStartup.ps1`

Se explicó que `Ready` significa que la tarea está habilitada y lista,
no que se esté ejecutando. Se pidió leer el script y revisar el tipo de
activador y última ejecución.

### Usuario

``` text
No solamente dame algo para que se desactive permanentemente y solo se ejecute cuando el dashboard este activo
```

### Asistente

Se propuso desactivar la tarea sin eliminarla:

``` powershell
Disable-ScheduledTask -TaskName "BankPulseAirflow"
```

y verificar:

``` powershell
Get-ScheduledTask -TaskName "BankPulseAirflow" | Select-Object TaskName, State
```

Se aclaró que la desactivación no detiene un proceso de Airflow que ya
esté funcionando y que la vinculación al dashboard requeriría configurar
el inicio y cierre de servicios.

### Usuario

``` text
17:14:57
Disable-ScheduledTask -TaskName "BankPulseAirflow"

TaskPath  TaskName         State
\         BankPulseAirflow D…

17:16:25
Get-ScheduledTask -TaskName "BankPulseAirflow" | Select-Object TaskName, State

TaskName          State
--------          -----
BankPulseAirflow  Disabled
```

### Asistente

Se confirmó que la tarea quedó desactivada y se solicitaron el contenido
del script y los contenedores activos para preparar la vinculación al
dashboard.

### Usuario

``` text
17:17:08
Get-Content "C:\Users\mimoe\OneDrive\Documentos\ProyectDataMining\BankPulseMlops\scripts\airflowAutoStartup.ps1"

param([datetime]$testDate)

$ErrorActionPreference = "Stop"

$wslPath = "C:\Program Files\WSL\wsl.exe"
$distributionName = "Ubuntu"
$logPath = Join-Path $PSScriptRoot "airflowAutoStartup.log"
$dagId = "bankPulsePipeline"
$airflowStartedByScript = $false
$airflowProcess = $null
$airflowLinuxPid = $null
$runCompleted = $false
$executionFailed = $false
$maxWaitMinutes = 180

function Write-Log {
    param([string]$message)

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $message"
    Write-Host $logEntry
    Add-Content -Path $logPath -Value $logEntry
}

function Invoke-AirflowCommand {
    param([string]$command)

    $commandParts = $command.Split(" ", [StringSplitOptions]::RemoveEmptyEntries)
    $result = & $wslPath -d $distributionName -- env AIRFLOW_HOME=/home/mimoe/airflowHome /home/mimoe/airflowEnvironment/bin/airflow @commandParts 2>$null

    if ($LASTEXITCODE -ne 0) {
        throw "Error ejecutando Airflow: $result"
    }

    return $result
}

function Test-AirflowRunning {
    & $wslPath -d $distributionName -- pgrep -f "[a]irflow standalone" 2>$null | Out-Null
    return ($LASTEXITCODE -eq 0)
}

function Test-AirflowReady {
    try {
        $client = [System.Net.Sockets.TcpClient]::new()
        $result = $client.BeginConnect("127.0.0.1", 8080, $null, $null)
        $connected = $result.AsyncWaitHandle.WaitOne(2000)

        if ($connected) {
            $client.EndConnect($result)
        }

        $client.Close()
        return $connected
    }
    catch {
        return $false
    }
}

function Test-SchedulerHealthy {
    try {
        Invoke-AirflowCommand 'jobs check --job-type SchedulerJob' | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Start-Airflow {
    Write-Log "Iniciando Airflow..."

    & $wslPath -d $distributionName -- rm -f /home/mimoe/airflowHome/bankPulseStandalone.pid
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo limpiar el archivo PID anterior."
    }

    $bashCommand = 'echo $$ > /home/mimoe/airflowHome/bankPulseStandalone.pid; exec env PATH=/home/mimoe/airflowEnvironment/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin AIRFLOW_HOME=/home/mimoe/airflowHome /home/mimoe/airflowEnvironment/bin/airflow standalone'

    $script:airflowProcess = Start-Process `
        -FilePath $wslPath `
        -ArgumentList @("-d", $distributionName, "--", "bash", "-lc", "`"$bashCommand`"") `
        -WindowStyle Hidden `
        -PassThru
    $script:airflowStartedByScript = $true

    for ($attempt = 1; $attempt -le 30; $attempt++) {
        $script:airflowLinuxPid = (& $wslPath -d $distributionName -- cat /home/mimoe/airflowHome/bankPulseStandalone.pid 2>$null | Select-Object -First 1)

        if ($script:airflowLinuxPid -match '^\d+$') {
            $processCommand = & $wslPath -d $distributionName -- ps -p $script:airflowLinuxPid -o args=

            if ($LASTEXITCODE -eq 0 -and $processCommand -match '/airflow standalone$') {
                break
            }
        }

        $script:airflowLinuxPid = $null

        Start-Sleep -Seconds 2
    }

    if (-not $script:airflowLinuxPid) {
        throw "No se pudo identificar el PID de Airflow despues de 60 segundos."
    }
    Write-Log "Airflow iniciado. PID Linux: $script:airflowLinuxPid"
}

function Get-MonthlyRun {
    $json = Invoke-AirflowCommand "dags list-runs $dagId --output json"
    $runs = @($json | ConvertFrom-Json -DateKind String)

    $targetDate = if ($null -ne $testDate -and $testDate -ne [datetime]::MinValue) { $testDate.Date } else { (Get-Date).Date }
    $mexicoTimeZone = [TimeZoneInfo]::FindSystemTimeZoneById("Central Standard Time (Mexico)")

    foreach ($run in $runs) {
        if ($run.run_id -notlike "scheduled__*") {
            continue
        }

        $runDate = [TimeZoneInfo]::ConvertTime(
            [DateTimeOffset]::Parse($run.run_after),
            $mexicoTimeZone
        )

        if ($runDate.Date -eq $targetDate -and $runDate.Hour -eq 20) {
            return $run
        }
    }

    return $null
}

try {
    Write-Log "Iniciando automatizacion mensual."

    $now = Get-Date

    if (-not $PSBoundParameters.ContainsKey("testDate") -and $now.Day -ne 1) {
        throw "La automatizacion solo debe ejecutarse el primer dia del mes."
    }

    if (Test-AirflowRunning) {
        throw "Airflow ya estaba iniciado. No se modificara la instancia existente."
    }

    Start-Airflow

    $deadline = (Get-Date).AddMinutes($maxWaitMinutes)

    while (-not (Test-AirflowReady) -or -not (Test-SchedulerHealthy)) {
        if ((Get-Date) -ge $deadline) {
            throw "Airflow no alcanzo un estado saludable."
        }

        Start-Sleep -Seconds 15
    }

    Write-Log "Airflow y scheduler disponibles."

    while ((Get-Date) -lt $deadline) {
        $run = Get-MonthlyRun

        if ($null -ne $run) {
            Write-Log "Estado del DAG: $($run.state)"

            if ($run.state -in @("success", "failed")) {
                Write-Log "Ejecucion mensual finalizada: $($run.state)"
                $runCompleted = $true

                if ($run.state -eq "failed") {
                    $executionFailed = $true
                    Write-Log "ERROR: El DAG mensual termino con estado failed."
                }

                break
            }
        }

        Start-Sleep -Seconds 30
    }

    if (-not $runCompleted) {
        throw "Tiempo maximo de espera alcanzado."
    }
}
catch {
    $executionFailed = $true
    Write-Log "ERROR: $($_.Exception.Message)"
}
finally {
    if ($airflowStartedByScript) {
        Write-Log "Solicitando apagado de Airflow..."

        if ($airflowLinuxPid) {
            if ($runCompleted) {
                $processCommand = & $wslPath -d $distributionName -- ps -p $airflowLinuxPid -o args=

                if ($LASTEXITCODE -eq 0 -and $processCommand -match '/airflow standalone$') {
                    & $wslPath -d $distributionName -- kill -TERM $airflowLinuxPid

                    if ($LASTEXITCODE -ne 0) {
                        throw "No se pudo solicitar el apagado de Airflow."
                    }

                    Write-Log "Se solicito el cierre del proceso principal de Airflow."
                }
                else {
                    Write-Log "No se detuvo ningun proceso: el PID ya no corresponde a Airflow."
                }

                & $wslPath -d $distributionName -- rm -f /home/mimoe/airflowHome/bankPulseStandalone.pid
            }
            else {
                Write-Log "Airflow permanece activo para evitar interrumpir una ejecucion pendiente."
            }
        }

        Write-Log "Automatizacion finalizada."
    }
}

if ($executionFailed) { exit 1 }
```

Después se ejecutó:

``` powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Resultado:

``` text
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine; check if the path is correct and if the daemon is running: open //./pipe/dockerDesktopLinuxEngine: El sistema no puede encontrar el archivo especificado.
```

### Asistente

Se explicó que `airflowAutoStartup.ps1` es un proceso de automatización
mensual que:

1.  Se ejecuta el primer día del mes.
2.  Inicia Airflow en Ubuntu mediante WSL.
3.  Espera a que Airflow y su scheduler estén disponibles.
4.  Supervisa el DAG `bankPulsePipeline`.
5.  Solicita apagar Airflow al finalizar correctamente.

Se señaló que no conviene reutilizarlo directamente para el dashboard
porque contiene restricciones de fecha y una lógica de espera de hasta
tres horas.

También se indicó que Docker Desktop no estaba ejecutándose o que su
motor Linux no estaba disponible. Se solicitaron:

``` powershell
wsl --list --verbose
```

``` powershell
Get-Process "Docker Desktop", "com.docker.backend" -ErrorAction SilentlyContinue | Select-Object ProcessName, Id
```

### Usuario

``` text
Aparte, antes detuve el localhost del dashboard, pero ya no pude cargar lo que tiene o, bueno, lo que llevamos.

17:17:43
wsl --list --verbose
NAME              STATE           VERSION
* docker-desktop    Stopped         2
  Ubuntu            Stopped         2

17:18:11
Get-Process "Docker Desktop", "com.docker.backend" -ErrorAction SilentlyContinue | Select-Object ProcessName, Id
```

### Asistente

Se explicó que detener el servidor de desarrollo de Vite hace que
`http://localhost:5173/` deje de cargar, pero no elimina los archivos
del dashboard. También se indicó que Ubuntu y Docker Desktop estaban
detenidos.

Se propuso recuperar el frontend sin iniciar Docker ni Airflow:

``` powershell
cd "C:\Users\mimoe\OneDrive\Documentos\ProyectDataMining\BankPulseMlops\frontend"
```

``` powershell
npm run dev
```

Cuando Vite muestre `http://localhost:5173/`, abrir esa dirección. Se
aclaró que los datos históricos estáticos del frontend deberían seguir
visibles, mientras que las funciones que dependan de FastAPI, Docker o
Airflow necesitarán esos servicios activos.

### Usuario

``` text
Dame la conversacion completa en un archivo .md
```

------------------------------------------------------------------------

## 3. Estado operativo al finalizar este tramo

-   Rama del proyecto: `feat/webDashboard`.
-   Tarea programada `BankPulseAirflow`: **Disabled**.
-   Script mensual existente: `scripts/airflowAutoStartup.ps1`.
-   El script mensual inicia Airflow en Ubuntu/WSL, supervisa el DAG
    `bankPulsePipeline` y puede solicitar el apagado al finalizar
    correctamente.
-   WSL mostraba `docker-desktop` y `Ubuntu` en estado `Stopped`.
-   Docker Desktop no estaba disponible al ejecutar `docker ps`.
-   La imagen `bankpulse-api:1.1.0` se construyó correctamente.
-   El contenedor anterior `bankpulseApi` se detuvo.
-   Se creó el contenedor nuevo `bankpulseApiV11` con la imagen `1.1.0`;
    todavía no se había confirmado su funcionamiento mediante pruebas
    HTTP en la información disponible.
-   El servidor Vite del dashboard se había detenido. Para recuperar la
    interfaz, se indicó entrar en `frontend` y ejecutar `npm run dev`.
-   Aún no se había implementado el inicio/parada coordinado de React,
    FastAPI y Airflow.
-   Aún no se había conectado el dashboard a fuentes dinámicas de
    métricas.

## 4. Próximas acciones pendientes

1.  Confirmar que Vite vuelve a cargar la interfaz en
    `http://localhost:5173/`.
2.  Iniciar Docker Desktop y comprobar el estado del contenedor
    `bankpulseApiV11`.
3.  Probar `http://localhost:8000/` y `http://localhost:8000/metrics`.
4.  Diseñar un mecanismo independiente para iniciar y detener los
    servicios necesarios al abrir/cerrar el dashboard.
5.  No volver a habilitar la tarea programada `BankPulseAirflow` para el
    arranque automático de Windows.
6.  Diseñar la integración del frontend con datos reales y estados
    explícitos cuando un servicio no esté disponible.
