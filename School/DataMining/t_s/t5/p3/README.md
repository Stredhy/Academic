# Proyecto 4: Dockerfile multietapa con R y Python

## 1. Necesidad del proyecto

Se requiere preparar datos con R y analizarlos con Python sin incluir ambas herramientas en la imagen final. Una construcción multietapa permite generar el archivo con R durante `docker build` y copiar solamente ese archivo a la etapa de Python.

## 2. Objetivo

Crear una imagen de Docker que genere `resultado.csv` con R y que, al ejecutar el contenedor, calcule con Python el promedio de las edades.

## 3. Requisitos

- Windows 11 con Docker Desktop instalado y **en ejecución** (motor Linux).
- PowerShell o terminal integrada de VS Code.
- Conexión a Internet para descargar las imágenes base la primera vez.

No es necesario instalar R ni Python localmente para ejecutar el proyecto con Docker.

## 4. Archivos incluidos

- `generar.R`: genera tres registros (Ana, Carlos y Laura), duplica las edades y escribe `resultado.csv`.
- `analizar.py`: abre el CSV con el módulo estándar `csv` de Python y calcula el promedio.
- `Dockerfile(2)`: primera etapa con `r-base:latest` y segunda con `python:3.12-slim`.
- `ejecutar.ps1`: automatiza la construcción y ejecución desde PowerShell (archivo auxiliar).

`resultado.csv` **no se crea manualmente**: aparece dentro de la imagen durante la construcción.

## 5. Abrir el proyecto

Descomprime el ZIP y abre la carpeta `proyecto4-docker-multietapa` en VS Code. Abre la terminal integrada de PowerShell dentro de esa carpeta.

Comprueba que Docker esté disponible:

```powershell
docker --version
docker info
```

## 6. Construir la imagen

El archivo se llama exactamente `Dockerfile(2)`, así que hay que especificarlo con `-f`:

```powershell
docker build -f "Dockerfile(2)" -t proyecto4-multietapa:latest .
```

Durante la construcción, R ejecuta `generar.R` y crea `/app/resultado.csv` en la etapa `build`. Docker copia ese archivo a la imagen final de Python.

## 7. Comprobar la imagen

```powershell
docker images proyecto4-multietapa
```

Debe aparecer la imagen con etiqueta `latest`.

## 8. Ejecutar el contenedor

```powershell
docker run --rm proyecto4-multietapa:latest
```

Resultado esperado:

- Edades: `[25, 31, 28]`
- Edad promedio: `28.0`

El contenedor termina al finalizar el programa. `--rm` elimina el contenedor temporal, pero no la imagen.

## 9. Comprobar el CSV

```powershell
docker run --rm proyecto4-multietapa:latest cat /app/resultado.csv
```

El CSV debe contener las columnas `nombre`, `edad` y `edad_doble`, con los registros de Ana, Carlos y Laura.

## 10. Comprobar que R no está en la imagen final

```powershell
docker run --rm --entrypoint sh proyecto4-multietapa:latest -c "command -v R || echo 'R no está instalado en la imagen final'"
```

La etapa final parte de Python y no conserva la instalación de R.

## 11. Ejecutar todo con un solo script (opcional)

Desde PowerShell, en la carpeta del proyecto:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\ejecutar.ps1
```

## 12. Modificar y reconstruir

Si modificas `generar.R`, `analizar.py` o `Dockerfile(2)`, reconstruye la imagen antes de ejecutarla:

```powershell
docker build -f "Dockerfile(2)" -t proyecto4-multietapa:latest .
docker run --rm proyecto4-multietapa:latest
```

## 13. Explicación del proceso

1. Docker inicia la etapa `build` basada en R.
2. Copia `generar.R` y ejecuta `Rscript generar.R` durante la **construcción** (`RUN`).
3. R genera el archivo `/app/resultado.csv` con las edades y sus dobles.
4. Docker inicia una etapa nueva basada en Python.
5. Copia `analizar.py` y el CSV generado desde la primera etapa (`COPY --from=build`).
6. Al **ejecutar** el contenedor, `CMD` inicia Python y se calcula el promedio.

**Conclusión:** el proyecto demuestra cómo compartir resultados entre lenguajes mediante una construcción multietapa, evitando conservar R en la imagen final.

## 14. Solución de problemas

- **Docker no se reconoce:** comprueba que Docker Desktop esté instalado y reinicia la terminal.
- **No se puede conectar al daemon:** inicia Docker Desktop y espera a que el motor esté listo.
- **No encuentra `resultado.csv` al ejecutar `analizar.py` localmente:** ese archivo se genera dentro de Docker durante `docker build`; ejecuta el contenedor como se indica arriba.
- **No encuentra el Dockerfile:** confirma que estás dentro de la carpeta del proyecto y que usas `-f "Dockerfile(2)"`.

## 15. Resultado final

Se obtiene una imagen que utiliza R solamente durante la construcción, ejecuta Python al iniciar y muestra un promedio de **28.0 años**. No se requieren bibliotecas externas de Python ni archivo `requirements.txt`.
