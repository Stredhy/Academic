# Utilizar una imagen que ya contiene Python 3.9.
FROM python:3.9-slim

# Establecer /app como directorio de trabajo
# dentro de la imagen.
WORKDIR /app

# Copiar requirements.txt desde la carpeta del proyecto
# en nuestra computadora hacia /app dentro de la imagen.
#
# Origen: requirements.txt de nuestra computadora.
# Destino: el punto ".", que representa /app porque
# anteriormente establecimos WORKDIR /app.
COPY requirements.txt .

# Instalar dentro de la imagen las dependencias
# indicadas en requirements.txt.
RUN pip install -r requirements.txt

# Copiar el contenido de la carpeta del proyecto
# en nuestra computadora hacia /app dentro de la imagen.
#
# Primer punto: carpeta actual de nuestra computadora.
# Segundo punto: directorio /app dentro de la imagen.
COPY . .

# Ejecutar el programa cuando inicie el contenedor.
CMD ["python", "processData.py"]