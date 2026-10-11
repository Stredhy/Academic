# ============================================================
# REGRESIÓN LOGÍSTICA
# Hotel Booking Cancellation
#
# Objetivo:
# Determinar si un cliente cancela o no su reservación.
#
# is_canceled:
# 0 = No cancela
# 1 = Cancela
# ============================================================


# ------------------------------------------------------------
# 1. LIBRERÍAS
# ------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm


# ------------------------------------------------------------
# 2. CARGAR DATASET
# ------------------------------------------------------------

df = pd.read_csv(
    "Python_Project_09_Random_Forest_Classification_Prospect_Hotel_Booking_Cancellation.csv"
)

print("Primeras filas:")
print(df.head())

print("\nTamaño del dataset:")
print(df.shape)


# ------------------------------------------------------------
# 3. VARIABLE OBJETIVO
# ------------------------------------------------------------

# is_canceled:
# 0 = No canceló
# 1 = Sí canceló

y = df["is_canceled"]


# ------------------------------------------------------------
# 4. SELECCIONAR VARIABLES CONTINUAS
# ------------------------------------------------------------

variables = [
    "lead_time",
    "arrival_date_year",
    "arrival_date_week_number",
    "arrival_date_day_of_month",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "booking_changes",
    "days_in_waiting_list",
    "adr",
    "required_car_parking_spaces",
    "total_of_special_requests"
]

X = df[variables].copy()


# ------------------------------------------------------------
# 5. LIMPIAR DATOS
# ------------------------------------------------------------

# Reemplazamos valores vacíos con la mediana
# de cada variable.

X = X.fillna(X.median())


# ------------------------------------------------------------
# 6. AGREGAR CONSTANTE
# ------------------------------------------------------------

# La constante representa el intercepto β0.

X = sm.add_constant(X)


# ------------------------------------------------------------
# 7. CREAR REGRESIÓN LOGÍSTICA
# ------------------------------------------------------------

modelo = sm.Logit(y, X)

resultado = modelo.fit()


# ------------------------------------------------------------
# 8. MOSTRAR RESULTADOS
# ------------------------------------------------------------

print("\n==============================================")
print("RESULTADOS DE LA REGRESIÓN LOGÍSTICA")
print("==============================================")

print(resultado.summary())


# ------------------------------------------------------------
# 9. OBTENER BETA Y VALOR P
# ------------------------------------------------------------

beta = resultado.params
valor_p = resultado.pvalues


print("\n==============================================")
print("BETA Y VALOR P")
print("==============================================")

for variable in beta.index:

    print(
        f"{variable:40} "
        f"Beta = {beta[variable]:.6f}   "
        f"p = {valor_p[variable]:.6f}"
    )


# ------------------------------------------------------------
# 10. DETERMINAR VARIABLES SIGNIFICATIVAS
# ------------------------------------------------------------

print("\n==============================================")
print("SIGNIFICANCIA DE LAS VARIABLES")
print("==============================================")

for variable in variables:

    if valor_p[variable] < 0.05:

        print(
            f"{variable}: SIGNIFICATIVA "
            f"(p = {valor_p[variable]:.6f})"
        )

    else:

        print(
            f"{variable}: NO SIGNIFICATIVA "
            f"(p = {valor_p[variable]:.6f})"
        )


# ------------------------------------------------------------
# 11. INTERPRETAR EL SIGNO DE BETA
# ------------------------------------------------------------

print("\n==============================================")
print("INTERPRETACIÓN DE BETA")
print("==============================================")

for variable in variables:

    if beta[variable] > 0:

        print(
            f"{variable}: aumenta la probabilidad "
            f"de cancelación."
        )

    else:

        print(
            f"{variable}: disminuye la probabilidad "
            f"de cancelación."
        )


# ------------------------------------------------------------
# 12. GRÁFICA LOGÍSTICA
# ------------------------------------------------------------

# Para representar la regresión logística
# utilizaremos lead_time.

variable_grafica = "lead_time"

x = df[variable_grafica].fillna(
    df[variable_grafica].median()
)

y_grafica = df["is_canceled"]


# Crear un modelo utilizando solamente lead_time.

X_log = sm.add_constant(x)

modelo_grafica = sm.Logit(
    y_grafica,
    X_log
)

resultado_grafica = modelo_grafica.fit(
    disp=False
)


# Crear valores para la curva.

x_valores = np.linspace(
    x.min(),
    x.max(),
    500
)


# Crear matriz con constante.

X_valores = sm.add_constant(
    x_valores
)


# Calcular probabilidades.

probabilidades = resultado_grafica.predict(
    X_valores
)


# ------------------------------------------------------------
# 13. DIBUJAR GRÁFICA
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

# Datos reales

plt.scatter(
    x,
    y_grafica,
    alpha=0.10
)

# Curva logística

plt.plot(
    x_valores,
    probabilidades,
    linewidth=3
)

# Línea del 50%

plt.axhline(
    0.5,
    linestyle="--"
)

plt.xlabel(
    "Lead Time (días)"
)

plt.ylabel(
    "Probabilidad de cancelación"
)

plt.title(
    "Regresión Logística: Lead Time vs Cancelación"
)

plt.yticks(
    [0, 0.5, 1],
    [
        "No cancela",
        "50%",
        "Cancela"
    ]
)

plt.grid()

plt.show()


# ------------------------------------------------------------
# 14. PREDICCIÓN DE UN CLIENTE
# ------------------------------------------------------------

# Cliente de ejemplo.

cliente = pd.DataFrame({

    "lead_time": [120],

    "arrival_date_year": [2017],

    "arrival_date_week_number": [30],

    "arrival_date_day_of_month": [15],

    "stays_in_weekend_nights": [2],

    "stays_in_week_nights": [4],

    "adults": [2],

    "children": [0],

    "babies": [0],

    "previous_cancellations": [1],

    "previous_bookings_not_canceled": [0],

    "booking_changes": [0],

    "days_in_waiting_list": [0],

    "adr": [150],

    "required_car_parking_spaces": [0],

    "total_of_special_requests": [0]
})


# Rellenar valores faltantes si existen.

cliente = cliente.fillna(
    X.drop(columns="const").median()
)


# Agregar constante.

cliente = sm.add_constant(
    cliente,
    has_constant="add"
)


# ------------------------------------------------------------
# 15. CALCULAR PROBABILIDAD
# ------------------------------------------------------------

probabilidad = resultado.predict(
    cliente
)[0]


print("\n==============================================")
print("PREDICCIÓN DEL CLIENTE")
print("==============================================")

print(
    f"Probabilidad de cancelación: "
    f"{probabilidad * 100:.2f}%"
)


# ------------------------------------------------------------
# 16. RESPUESTA FINAL
# ------------------------------------------------------------

if probabilidad >= 0.50:

    print(
        "\n¿Este cliente te va a dejar plantado?"
    )

    print(
        "SÍ, probablemente cancelará."
    )

else:

    print(
        "\n¿Este cliente te va a dejar plantado?"
    )

    print(
        "NO, probablemente NO cancelará."
    )