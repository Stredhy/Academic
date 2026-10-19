# ============================================================
# MINERÍA DE DATOS - TAREA 1
# Ejercicios con Pandas
# Dataset: student-mat.csv
# ============================================================


# ============================================================
# LIBRERÍAS
# ============================================================

# Pandas:
# Sirve para trabajar con tablas y datos.
import pandas as pd

# NumPy:
# Sirve para operaciones numéricas y generación de valores
# aleatorios.
import numpy as np

# Matplotlib:
# Sirve para crear gráficas.
import matplotlib.pyplot as plt

# Seaborn:
# Sirve para crear gráficas estadísticas.
import seaborn as sns


# ============================================================
# 1. IMPORTACIÓN Y EXPLORACIÓN
# ============================================================

# ------------------------------------------------------------
# 1.A
# Carga el archivo student-mat.csv en un DataFrame.
# ------------------------------------------------------------

df = pd.read_csv("student-mat.csv")


# ------------------------------------------------------------
# 1.B
# Crea una columna llamada student_id utilizando
# el índice original del DataFrame.
# ------------------------------------------------------------

df["student_id"] = df.index


# ------------------------------------------------------------
# 1.C
# Revisa las dimensiones de la tabla.
# El resultado tiene la forma:
#
# (número de filas, número de columnas)
# ------------------------------------------------------------

print("\n===== 1.C DIMENSIONES =====")
print(df.shape)


# ------------------------------------------------------------
# 1.D
# Identifica el tipo de dato de cada columna.
# ------------------------------------------------------------

print("\n===== 1.D TIPOS DE DATOS =====")
print(df.dtypes)


# ------------------------------------------------------------
# 1.E
# Muestra las primeras 10 filas del DataFrame.
# ------------------------------------------------------------

print("\n===== 1.E PRIMERAS 10 FILAS =====")
print(df.head(10))


# ------------------------------------------------------------
# 1.F
# Obtiene estadísticas descriptivas de las columnas
# numéricas.
#
# Incluye:
# - cantidad de datos
# - promedio
# - desviación estándar
# - mínimo
# - cuartiles
# - máximo
# ------------------------------------------------------------

print("\n===== 1.F ESTADÍSTICAS DESCRIPTIVAS =====")
print(df.describe())


# ============================================================
# 2. LIMPIEZA DE DATOS
# ============================================================

# ------------------------------------------------------------
# 2.A
# Selecciona aleatoriamente el 5% de las posiciones del
# DataFrame solamente en columnas numéricas y las reemplaza
# por valores nulos (NaN).
# ------------------------------------------------------------

# Obtiene las columnas que contienen datos numéricos.
numeric_columns = df.select_dtypes(include="number").columns

# student_id NO se modifica porque es nuestro identificador
# interno.
numeric_columns = numeric_columns.drop("student_id")


# Convertimos las columnas numéricas a float para poder
# almacenar valores NaN sin problemas.
df[numeric_columns] = df[numeric_columns].astype(float)


# Calculamos el número total de posiciones disponibles.
total_positions = len(df) * len(numeric_columns)


# Calculamos el 5% de esas posiciones.
number_of_nan = int(total_positions * 0.05)


# Creamos un generador de números aleatorios.
# El 42 hace que podamos obtener los mismos resultados
# si ejecutamos nuevamente el programa.
rng = np.random.default_rng(42)


# Seleccionamos posiciones aleatorias sin repetir.
random_positions = rng.choice(
    total_positions,
    size=number_of_nan,
    replace=False
)


# Convertimos cada posición seleccionada en:
# - una fila
# - una columna
#
# Después reemplazamos ese valor por NaN.
for position in random_positions:

    row = position // len(numeric_columns)

    column = position % len(numeric_columns)

    df.loc[df.index[row], numeric_columns[column]] = np.nan


# ------------------------------------------------------------
# 2.B.a
# Cuenta la cantidad de valores nulos por columna.
# ------------------------------------------------------------

print("\n===== 2.B.a NULOS POR COLUMNA =====")
print(df.isnull().sum())


# ------------------------------------------------------------
# 2.B.b
# Cuenta la cantidad de valores nulos por fila.
# ------------------------------------------------------------

print("\n===== 2.B.b NULOS POR FILA =====")
print(df.isnull().sum(axis=1))


# ------------------------------------------------------------
# 2.C.a
# Si el valor nulo está en alguna columna categórica clave:
#
# - sex
# - school
# - address
#
# se elimina la fila completa.
# ------------------------------------------------------------

categorical_key_columns = [
    "sex",
    "school",
    "address"
]

df = df.dropna(
    subset=categorical_key_columns
)


# ------------------------------------------------------------
# 2.C.b
# Si el valor nulo está en las columnas numéricas:
#
# - age
# - G1
# - G2
# - G3
# - Dalc
# - Walc
#
# se reemplaza por la mediana correspondiente.
# ------------------------------------------------------------

numeric_columns_to_fill = [
    "age",
    "G1",
    "G2",
    "G3",
    "Dalc",
    "Walc"
]


for column in numeric_columns_to_fill:

    df[column] = df[column].fillna(
        df[column].median()
    )


# ------------------------------------------------------------
# 2.D
# Verifica que ya no existan valores nulos.
#
# Si todo salió correctamente, las columnas deberían
# mostrar 0.
# ------------------------------------------------------------

print("\n===== 2.D NULOS DESPUÉS DE LA LIMPIEZA =====")
print(df.isnull().sum())


# ============================================================
# 3. FILTRADO Y SELECCIÓN
# ============================================================

# ------------------------------------------------------------
# 3.A
# Crea una columna llamada avg_grade.
#
# Se calcula utilizando:
#
# (G1 + G2 + G3) / 3
# ------------------------------------------------------------

df["avg_grade"] = (
    df["G1"] +
    df["G2"] +
    df["G3"]
) / 3


# ------------------------------------------------------------
# 3.B
# Selecciona a los estudiantes cuyo promedio final
# (avg_grade) sea mayor a 12.
# ------------------------------------------------------------

students_over_12 = df[
    df["avg_grade"] > 12
]


print("\n===== 3.B PROMEDIO MAYOR A 12 =====")

print(
    students_over_12[
        [
            "student_id",
            "G1",
            "G2",
            "G3",
            "avg_grade"
        ]
    ]
)


# ------------------------------------------------------------
# 3.C
# Selecciona a los estudiantes con consumo alto de alcohol
# durante el fin de semana.
#
# Walc >= 4
# ------------------------------------------------------------

students_high_alcohol = df[
    df["Walc"] >= 4
]


print("\n===== 3.C CONSUMO ALTO DE ALCOHOL =====")

print(
    students_high_alcohol[
        [
            "student_id",
            "Walc"
        ]
    ]
)


# ------------------------------------------------------------
# 3.D
# Calcula la mediana del tiempo de estudio.
# ------------------------------------------------------------

studytime_median = df["studytime"].median()


# Selecciona estudiantes cuyo tiempo de estudio sea mayor
# que la mediana.
students_high_studytime = df[
    df["studytime"] > studytime_median
]


print("\n===== 3.D TIEMPO DE ESTUDIO =====")

print("Mediana de studytime:", studytime_median)

print(
    students_high_studytime[
        [
            "student_id",
            "studytime"
        ]
    ]
)


# ============================================================
# 4. CREACIÓN DE COLUMNAS NUEVAS
# ============================================================

# ------------------------------------------------------------
# 4.A
# Crea una columna llamada high_alcohol.
#
# Será True si:
#
# Dalc + Walc >= 6
#
# y False en caso contrario.
# ------------------------------------------------------------

df["high_alcohol"] = (
    df["Dalc"] +
    df["Walc"]
) >= 6


print("\n===== 4.A HIGH_ALCOHOL =====")

print(
    df[
        [
            "student_id",
            "Dalc",
            "Walc",
            "high_alcohol"
        ]
    ].head(10)
)


# ------------------------------------------------------------
# 4.B
# Crea una columna llamada alcohol_category.
#
# Reglas:
#
# Low:
# Dalc + Walc <= 3
#
# Moderate:
# Dalc + Walc entre 4 y 5
#
# High:
# Dalc + Walc >= 6
# ------------------------------------------------------------

alcohol_total = (
    df["Dalc"] +
    df["Walc"]
)


df["alcohol_category"] = pd.cut(
    alcohol_total,
    bins=[
        -float("inf"),
        3,
        5,
        float("inf")
    ],
    labels=[
        "Low",
        "Moderate",
        "High"
    ]
)


print("\n===== 4.B ALCOHOL_CATEGORY =====")

print(
    df[
        [
            "student_id",
            "Dalc",
            "Walc",
            "alcohol_category"
        ]
    ].head(10)
)


# ============================================================
# 5. AGRUPACIONES
# ============================================================

# ------------------------------------------------------------
# 5.A
# Calcula el promedio de avg_grade por sexo.
# ------------------------------------------------------------

avg_grade_by_sex = (
    df
    .groupby("sex")["avg_grade"]
    .mean()
)


print("\n===== 5.A PROMEDIO DE AVG_GRADE POR SEXO =====")

print(avg_grade_by_sex)


# ------------------------------------------------------------
# 5.B
# Calcula la mediana de Walc por sexo.
# ------------------------------------------------------------

median_walc_by_sex = (
    df
    .groupby("sex")["Walc"]
    .median()
)


print("\n===== 5.B MEDIANA DE WALC POR SEXO =====")

print(median_walc_by_sex)


# ------------------------------------------------------------
# 5.C
# Calcula el número de estudiantes por categoría de alcohol.
# ------------------------------------------------------------

students_by_alcohol_category = (
    df["alcohol_category"]
    .value_counts()
    .sort_index()
)


print("\n===== 5.C ESTUDIANTES POR CATEGORÍA DE ALCOHOL =====")

print(students_by_alcohol_category)


# ------------------------------------------------------------
# 5.D
# Calcula el promedio del tiempo de estudio por categoría
# de alcohol.
# ------------------------------------------------------------

avg_studytime_by_alcohol = (
    df
    .groupby("alcohol_category")["studytime"]
    .mean()
)


print("\n===== 5.D PROMEDIO DE STUDYTIME POR ALCOHOL =====")

print(avg_studytime_by_alcohol)


# ============================================================
# 6. ORDENAMIENTO Y TOP-N
# ============================================================

# ------------------------------------------------------------
# 6.A
# Ordena a los estudiantes por avg_grade de mayor a menor.
# ------------------------------------------------------------

df_sorted = df.sort_values(
    by="avg_grade",
    ascending=False
)


print("\n===== 6.A ESTUDIANTES ORDENADOS =====")

print(
    df_sorted[
        [
            "student_id",
            "avg_grade"
        ]
    ].head(10)
)


# ------------------------------------------------------------
# 6.B
# Selecciona los 10 estudiantes con mayor avg_grade
# y los guarda en un DataFrame llamado top10.
# ------------------------------------------------------------

top10 = df_sorted.head(10).copy()


print("\n===== 6.B TOP 10 =====")

print(
    top10[
        [
            "student_id",
            "avg_grade"
        ]
    ]
)


# ------------------------------------------------------------
# 6.C
# Selecciona los 10 estudiantes con menor avg_grade
# y los guarda en un DataFrame llamado bottom10.
# ------------------------------------------------------------

bottom10 = df_sorted.tail(10).copy()


print("\n===== 6.C BOTTOM 10 =====")

print(
    bottom10[
        [
            "student_id",
            "avg_grade"
        ]
    ]
)


# ============================================================
# 7. INTEGRACIÓN DE RESULTADOS
#    CONCAT Y MERGE
# ============================================================

# ------------------------------------------------------------
# 7.A
# Para top10 agrega una columna llamada "grupo"
# con el valor "top".
# ------------------------------------------------------------

top10["grupo"] = "top"


# Para bottom10 agrega una columna llamada "grupo"
# con el valor "bottom".
bottom10["grupo"] = "bottom"


# Concatenamos los dos DataFrames.
#
# El resultado tendrá los 10 mejores + los 10 peores
# estudiantes.
ranking20 = pd.concat(
    [
        top10,
        bottom10
    ],
    ignore_index=True
)


print("\n===== 7.A RANKING20 =====")

print(
    ranking20[
        [
            "student_id",
            "avg_grade",
            "grupo"
        ]
    ]
)


# ------------------------------------------------------------
# 7.B
# Crea un DataFrame llamado resumen_sex.
#
# Para cada sexo calcula:
#
# - promedio de avg_grade
# - promedio de Walc
# - promedio de Dalc
# ------------------------------------------------------------

resumen_sex = (
    df
    .groupby("sex")
    .agg(
        promedio_avg_grade=("avg_grade", "mean"),
        promedio_Walc=("Walc", "mean"),
        promedio_Dalc=("Dalc", "mean")
    )
    .reset_index()
)


print("\n===== 7.B RESUMEN_SEX =====")

print(resumen_sex)


# ------------------------------------------------------------
# 7.C
# Realiza un merge entre ranking20 y resumen_sex.
#
# La columna "sex" será utilizada como clave.
#
# how="left":
# Conserva todos los estudiantes de ranking20.
# ------------------------------------------------------------

ranking20_enriquecido = pd.merge(
    ranking20,
    resumen_sex,
    on="sex",
    how="left"
)


print("\n===== 7.C RANKING20_ENRIQUECIDO =====")

print(ranking20_enriquecido)


# ------------------------------------------------------------
# 7.D
# Indica cuántas filas y columnas tiene:
#
# - ranking20
# - ranking20_enriquecido
# ------------------------------------------------------------

print("\n===== 7.D DIMENSIONES =====")

print(
    "ranking20:",
    ranking20.shape
)

print(
    "ranking20_enriquecido:",
    ranking20_enriquecido.shape
)


# ============================================================
# 8. CRUCE DE VARIABLES
# ============================================================

# ------------------------------------------------------------
# 8.A
# Genera una tabla cruzada entre:
#
# sex
# alcohol_category
#
# mostrando el número de estudiantes de cada grupo.
# ------------------------------------------------------------

crosstab_sex_alcohol = pd.crosstab(
    df["sex"],
    df["alcohol_category"]
)


print("\n===== 8.A SEX VS ALCOHOL_CATEGORY =====")

print(crosstab_sex_alcohol)


# ------------------------------------------------------------
# 8.B
# Genera una tabla cruzada entre:
#
# alcohol_category
# studytime
# ------------------------------------------------------------

crosstab_alcohol_studytime = pd.crosstab(
    df["alcohol_category"],
    df["studytime"]
)


print("\n===== 8.B ALCOHOL_CATEGORY VS STUDYTIME =====")

print(crosstab_alcohol_studytime)


# ============================================================
# 9. EXPORTACIÓN
# ============================================================

# ------------------------------------------------------------
# 9.A
# Guarda el DataFrame top10 en un archivo CSV.
# ------------------------------------------------------------

top10.to_csv(
    "top10.csv",
    index=False
)


# ------------------------------------------------------------
# 9.B
# Guarda el DataFrame bottom10 en un archivo CSV.
# ------------------------------------------------------------

bottom10.to_csv(
    "bottom10.csv",
    index=False
)


# ------------------------------------------------------------
# 9.C
# Guarda el DataFrame ranking20 en un archivo CSV.
# ------------------------------------------------------------

ranking20.to_csv(
    "ranking20.csv",
    index=False
)


# ------------------------------------------------------------
# 9.D
# Guarda el DataFrame ranking20_enriquecido en un archivo CSV.
# ------------------------------------------------------------

ranking20_enriquecido.to_csv(
    "ranking20_enriquecido.csv",
    index=False
)


print("\n===== 9. ARCHIVOS EXPORTADOS =====")

print("top10.csv")
print("bottom10.csv")
print("ranking20.csv")
print("ranking20_enriquecido.csv")


# ============================================================
# 10. VISUALIZACIÓN Y ANÁLISIS DE DATOS
# ============================================================

# Esta sección NO sustituye los puntos anteriores.
# Es una sección adicional para practicar visualización
# y análisis de datos.


# ------------------------------------------------------------
# 10.A
# Histograma de los promedios finales.
#
# Permite observar cómo se distribuyen las calificaciones
# de los estudiantes.
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="avg_grade",
    bins=15,
    kde=True
)

plt.title(
    "Distribución del promedio final"
)

plt.xlabel(
    "Promedio final"
)

plt.ylabel(
    "Cantidad de estudiantes"
)

plt.tight_layout()

plt.show()


# ------------------------------------------------------------
# 10.B
# Relación entre tiempo de estudio y promedio.
#
# El boxplot permite comparar la distribución de las
# calificaciones para cada nivel de studytime.
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="studytime",
    y="avg_grade"
)

plt.title(
    "Tiempo de estudio vs promedio final"
)

plt.xlabel(
    "Tiempo de estudio"
)

plt.ylabel(
    "Promedio final"
)

plt.tight_layout()

plt.show()


# ------------------------------------------------------------
# 10.C
# Cantidad de estudiantes por categoría de alcohol.
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="alcohol_category"
)

plt.title(
    "Estudiantes por categoría de consumo de alcohol"
)

plt.xlabel(
    "Categoría de alcohol"
)

plt.ylabel(
    "Cantidad de estudiantes"
)

plt.tight_layout()

plt.show()


# ------------------------------------------------------------
# 10.D
# Promedio de calificaciones por sexo.
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="sex",
    y="avg_grade"
)

plt.title(
    "Promedio de calificación por sexo"
)

plt.xlabel(
    "Sexo"
)

plt.ylabel(
    "Promedio final"
)

plt.tight_layout()

plt.show()


# ------------------------------------------------------------
# 10.E
# Consumo de alcohol entre semana (Dalc) vs promedio.
#
# Permite observar cómo se distribuyen las calificaciones
# según el nivel de consumo entre semana.
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="Dalc",
    y="avg_grade"
)

plt.title(
    "Consumo de alcohol entre semana vs promedio"
)

plt.xlabel(
    "Dalc"
)

plt.ylabel(
    "Promedio final"
)

plt.tight_layout()

plt.show()


# ------------------------------------------------------------
# 10.F
# Consumo de alcohol durante el fin de semana (Walc)
# vs promedio.
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="Walc",
    y="avg_grade"
)

plt.title(
    "Consumo de alcohol en fin de semana vs promedio"
)

plt.xlabel(
    "Walc"
)

plt.ylabel(
    "Promedio final"
)

plt.tight_layout()

plt.show()


# ------------------------------------------------------------
# 10.G
# Relación entre tiempo de estudio y promedio mediante
# un scatter plot.
#
# Cada punto representa un estudiante.
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="studytime",
    y="avg_grade",
    hue="alcohol_category"
)

plt.title(
    "Tiempo de estudio vs promedio según consumo de alcohol"
)

plt.xlabel(
    "Tiempo de estudio"
)

plt.ylabel(
    "Promedio final"
)

plt.tight_layout()

plt.show()


# ------------------------------------------------------------
# 10.H
# Matriz de correlación.
#
# La correlación indica qué tan relacionadas están
# las variables numéricas.
#
# Valores cercanos a:
# +1 -> relación positiva fuerte
#  0 -> poca relación lineal
# -1 -> relación negativa fuerte
# ------------------------------------------------------------

numeric_df = df.select_dtypes(
    include="number"
)

correlation = numeric_df.corr()


plt.figure(figsize=(14, 10))

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)

plt.title(
    "Matriz de correlación de variables numéricas"
)

plt.tight_layout()

plt.show()


# ============================================================
# FIN DEL PROGRAMA
# ============================================================

print("\n===== PROGRAMA TERMINADO =====")