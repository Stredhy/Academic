# Partimos de una imagen que ya tiene Python 3.9 instalado.
FROM python:3.9-slim


# Creamos/seleccionamos /app como directorio de trabajo
# dentro de la imagen.
WORKDIR /app


# Copiamos primero requirements.txt desde nuestro proyecto
# hacia /app dentro de la imagen.
COPY requirements.txt .


# Instalamos las librerías que necesita nuestra aplicación:
# Flask y mysql-connector-python.
#
# Esto ocurre durante:
# docker build
RUN pip install -r requirements.txt


# Copiamos el resto del proyecto dentro de /app.
#
# Aquí entrarán:
# app.py
# init.sql
# templates/
# static/
# etc.
COPY . .


# Este será el comando por defecto cuando se cree
# y arranque un contenedor a partir de esta imagen.
#
# Equivale a ejecutar:
# python app.py
CMD ["python", "app.py"]