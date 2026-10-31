# Crear un pequeño conjunto de datos
datos <- data.frame(
  nombre = c("Ana", "Carlos", "Laura"),
  edad = c(25, 31, 28)
)

# Crear una nueva columna
datos$edad_doble <- datos$edad * 2

# Guardar el resultado
write.csv(
  datos,
  "resultado.csv",
  row.names = FALSE
)

print("resultado.csv creado correctamente")
