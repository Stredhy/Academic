# ============================================
# ETAPA 1: BUILD
# ============================================

# Utilizar Python 3.12 Slim para la etapa de construcción y nombrarla "build".
FROM python:3.12-slim AS build

# Crear y establecer /app como directorio de trabajo durante la etapa de construcción.
WORKDIR /app

# Copiar requirements.txt desde la carpeta del proyecto hacia /app.
COPY requirements.txt .

# Instalar las dependencias indicadas en requirements.txt.
# --no-cache-dir evita almacenar la caché utilizada por pip.
# --prefix=/install instala las dependencias dentro de /install.
# -r requirements.txt indica el archivo que contiene las dependencias.
RUN pip install \
    --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


# ============================================
# ETAPA 2: EJECUCIÓN
# ============================================

# Crear una nueva etapa limpia basada nuevamente en Python 3.12 Slim.
FROM python:3.12-slim

# Crear y establecer /app como directorio de trabajo de la imagen final.
WORKDIR /app

# Copiar únicamente las dependencias instaladas en /install durante la etapa build
# hacia /usr/local de la imagen final.
COPY --from=build /install /usr/local

# Copiar script.py desde la carpeta del proyecto hacia /app de la imagen final.
COPY script.py .

# Copiar data.csv desde la carpeta del proyecto hacia /app de la imagen final.
COPY data.csv .

# Ejecutar script.py automáticamente cuando se inicie el contenedor.
CMD ["python", "script.py"]