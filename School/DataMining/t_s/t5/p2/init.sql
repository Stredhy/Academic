-- Creamos la tabla usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    edad INT
);

-- Insertamos algunos datos iniciales
INSERT INTO usuarios (nombre, edad)
VALUES
    ('Ana', 25),
    ('Carlos', 31),
    ('Laura', 28);     