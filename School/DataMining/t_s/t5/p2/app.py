# Importamos Flask para crear la aplicación web.
# render_template nos permitirá cargar archivos HTML.
from importlib import import_module

try:
    flask = import_module("flask")
    Flask = flask.Flask
    render_template = flask.render_template
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Falta Flask. Instálalo con: python -m pip install Flask"
    ) from exc

# Librería para conectarnos desde Python a MySQL.
try:
    mysql_connector = import_module("mysql.connector")
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Falta mysql-connector-python. Instálalo con: "
        "python -m pip install mysql-connector-python"
    ) from exc


# ============================================================
# AQUÍ USAMOS __name__ EXPLÍCITAMENTE
# ============================================================
#
# Python establece automáticamente __name__.
#
# Flask recibe ese valor y lo utiliza, entre otras cosas,
# para determinar la ubicación raíz de nuestra aplicación.
#
app = Flask(__name__)


# ============================================================
# EXPERIMENTO PARA VER QUÉ HIZO FLASK CON __name__
# ============================================================

# Mostramos el valor que Python le dio a __name__.
print("Valor de __name__:", __name__)

# Mostramos la ruta raíz que Flask determinó.
#
# Cuando ejecutemos esto dentro de Docker,
# probablemente veremos:
#
# /app
#
print("Ruta raíz detectada por Flask:", app.root_path)

# Flask busca las plantillas, por defecto,
# en una carpeta llamada "templates".
print("Carpeta de templates:", app.template_folder)

# Flask también utiliza por defecto una carpeta
# llamada "static" para CSS, imágenes, JavaScript, etc.
print("Carpeta static:", app.static_folder)


# ============================================================
# CONEXIÓN CON MYSQL
# ============================================================

def get_db_connection():

    # Nos conectamos al servidor MySQL.
    #
    # IMPORTANTE:
    # "db" todavía tendrá sentido gracias a Docker Compose.
    # Compose creará un servicio llamado "db".
    connection = mysql_connector.connect(
        host="db",
        user="root",
        password="example",
        database="test_db"
    )

    # Devolvemos el objeto Connection.
    return connection


# ============================================================
# RUTA PRINCIPAL
# ============================================================

# "/" significa:
#
# http://localhost:5000/
#
# NO significa /usuarios.
#
# Cuando llegue una petición a "/",
# Flask ejecutará la función usuarios().
@app.route("/")
def usuarios():

    # Obtenemos una conexión con MySQL.
    connection = get_db_connection()

    # Creamos un cursor para poder ejecutar SQL.
    cursor = connection.cursor()

    # Enviamos esta consulta al servidor MySQL.
    cursor.execute(
        "SELECT nombre, edad FROM usuarios"
    )

    # Recuperamos TODAS las filas producidas
    # por la consulta anterior.
    #
    # resultados podría quedar así:
    #
    # [
    #     ("Ana", 25),
    #     ("Carlos", 31),
    #     ("Laura", 28)
    # ]
    resultados = cursor.fetchall()

    # Cerramos el cursor.
    cursor.close()

    # Cerramos la conexión con MySQL.
    connection.close()


    # ========================================================
    # AQUÍ VEMOS UNA CONSECUENCIA DEL Flask(__name__)
    # ========================================================
    #
    # Nosotros solamente escribimos:
    #
    # "usuarios.html"
    #
    # Flask ya conoce:
    #
    # app.root_path
    #
    # y sabe que por defecto las plantillas están en:
    #
    # templates/
    #
    # Por eso puede localizar:
    #
    # app.root_path
    #       +
    # templates/
    #       +
    # usuarios.html
    #
    # Dentro de Docker probablemente será:
    #
    # /app/templates/usuarios.html
    #
    return render_template(
        "usuarios.html",

        # Mandamos "resultados" al HTML con
        # el nombre "usuarios".
        usuarios=resultados
    )


# ============================================================
# AQUÍ USAMOS __name__ EXPLÍCITAMENTE POR SEGUNDA VEZ
# ============================================================
#
# Si ejecutamos:
#
# python app.py
#
# Python establece:
#
# __name__ = "__main__"
#
# Por lo tanto entra en este if.
#
if __name__ == "__main__":

    # Arrancamos Flask.
    #
    # 0.0.0.0 permite recibir conexiones
    # desde fuera del contenedor.
    #
    # Como no indicamos port=,
    # Flask utiliza 5000 por defecto.
    app.run(host="0.0.0.0")