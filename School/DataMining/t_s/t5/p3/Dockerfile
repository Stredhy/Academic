# ============================================================
# ETAPA 1: PROCESAMIENTO CON R
# ============================================================

FROM r-base:latest AS build

WORKDIR /app

# Copiar el script de R
COPY generar.R .

# Ejecutar R y generar resultado.csv durante la creación de la imagen
RUN Rscript generar.R


# ============================================================
# ETAPA 2: ANÁLISIS CON PYTHON
# ============================================================

FROM python:3.12-slim

WORKDIR /app

# Copiar el programa de Python
COPY analizar.py .

# Copiar únicamente el resultado generado por R
COPY --from=build /app/resultado.csv .

# Ejecutar Python cuando inicie el contenedor
CMD ["python", "analizar.py"]
