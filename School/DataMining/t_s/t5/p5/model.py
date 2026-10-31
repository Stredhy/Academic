import sys
import importlib
import numpy as np

try:
    tf = importlib.import_module("tensorflow")
except ModuleNotFoundError as exc:
    if exc.name == "tensorflow":
        raise SystemExit(
            "TensorFlow is not installed in this Python environment. "
            "Install it with: python -m pip install tensorflow"
        ) from exc
    raise

# Verificar que se proporcionó una imagen
if len(sys.argv) < 2:
    print("Uso: python model.py <ruta_imagen>")
    sys.exit(1)

ruta_imagen = sys.argv[1]

print("Cargando modelo...")

model = tf.keras.applications.MobileNetV2(
    weights="imagenet"
)

print("Cargando imagen:", ruta_imagen)

# Cargar y redimensionar la imagen
img = tf.keras.utils.load_img(
    ruta_imagen,
    target_size=(224, 224)
)

# Convertir imagen a arreglo numérico
img_array = tf.keras.utils.img_to_array(img)

# Agregar dimensión para formar un batch
img_array = np.expand_dims(img_array, axis=0)

# Preparar los valores para MobileNetV2
img_array = tf.keras.applications.mobilenet_v2.preprocess_input(
    img_array
)

# Hacer predicción
predicciones = model.predict(img_array)

# Obtener las 3 mejores predicciones
resultados = tf.keras.applications.mobilenet_v2.decode_predictions(
    predicciones,
    top=3
)[0]

print("\nPredicciones:")

for _, nombre, probabilidad in resultados:
    print(f"{nombre}: {probabilidad * 100:.2f}%")