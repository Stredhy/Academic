# Utilizar una imagen que ya incluye Python y TensorFlow.
FROM tensorflow/tensorflow:latest

# Establecer /app como el directorio de trabajo del contenedor.
WORKDIR /app

# Instalar Pillow para poder abrir y procesar archivos de imagen.
RUN pip install --no-cache-dir pillow

# Copiar model.py desde la carpeta del proyecto hacia /app.
COPY model.py .

# Ejecutar model.py y permitir agregar la ruta de la imagen como argumento.
ENTRYPOINT ["python", "model.py"]