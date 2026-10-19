# Importar Pandas.
import pandas as pd

# Leer los datos del archivo CSV.
df = pd.read_csv("data.csv")

# Mostrar las estadísticas descriptivas
# de las columnas nuls -lh python-script.tarméricas.
print(df.describe())