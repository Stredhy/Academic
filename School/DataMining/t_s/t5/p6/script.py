import pandas as pd

df = pd.read_csv("data.csv")

print("Datos:")
print(df.head())

print("\nEdad promedio:")
print(df["edad"].mean())