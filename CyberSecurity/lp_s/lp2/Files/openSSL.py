from docx import Document

doc = Document()
doc.add_heading("Reporte de Práctica: Uso de OpenSSL en Entorno Linux", level=1)

# Introducción
doc.add_heading("Introducción y Objetivo General", level=2)
doc.add_paragraph(
    "El presente reporte detalla la implementación y los resultados obtenidos al aplicar "
    "conceptos fundamentales de criptografía utilizando la herramienta OpenSSL en un entorno de Kali Linux[cite: 1]. "
    "Los objetivos principales consisten en comprender la generación de pares de claves asimétricas, el cifrado y "
    "descifrado de archivos, la validación de integridad mediante hashes y la aplicación de firmas digitales[cite: 2]."
)

# Parte 1
doc.add_heading("Parte 1: Generación de Pares de Claves (RSA)", level=2)
doc.add_paragraph(
    "Se estableció la base de la criptografía asimétrica mediante la creación de una clave privada RSA "
    "protegida con cifrado y su respectiva clave pública[cite: 1]."
)
doc.add_paragraph("• Creación de la clave privada: Algoritmo RSA de 2048 bits con protección AES-256[cite: 1].", style='List Bullet')
doc.add_paragraph("• Extracción de la clave pública: Componente público derivado para permitir cifrado externo[cite: 1].", style='List Bullet')

# Parte 2
doc.add_heading("Parte 2: Cifrado y Descifrado de Archivos (Asimétrico)", level=2)
doc.add_paragraph(
    "Se manipuló un archivo de texto para comprobar la confidencialidad utilizando criptografía de clave pública[cite: 1]."
)
doc.add_paragraph("• Archivo original: Creación de secreto.txt[cite: 1].", style='List Bullet')
doc.add_paragraph("• Cifrado: Uso de clave_publica.pem para generar secreto_cifrado.bin[cite: 1].", style='List Bullet')
doc.add_paragraph("• Descifrado: Uso de clave_privada.pem para recuperar secreto_descifrado.txt y validación con diff[cite: 1].", style='List Bullet')

# Parte 3
doc.add_heading("Parte 3: Cifrado Simétrico (AES-256-CBC)", level=2)
doc.add_paragraph(
    "Se aplicó cifrado simétrico con clave compartida mediante AES-256-CBC para proteger la información de forma eficiente[cite: 2]."
)

# Parte 4
doc.add_heading("Parte 4: Verificación de Integridad (Hashing)", level=2)
doc.add_paragraph(
    "Se implementó la función hash criptográfica SHA256 para comprobar que los archivos no sufrieron alteraciones[cite: 2]."
)

# Parte 5
doc.add_heading("Parte 5: Firma Digital y Verificación", level=2)
doc.add_paragraph(
    "Se generó una firma digital con la clave privada y se validó su autenticidad empleando la clave pública[cite: 2]."
)

# Conclusiones
doc.add_heading("Conclusiones", level=2)
doc.add_paragraph(
    "El uso de OpenSSL demostró ser una solución robusta y versátil para garantizar la confidencialidad, "
    "integridad y autenticidad de la información en entornos Linux[cite: 1, 2]."
)

doc.save("Reporte_OpenSSL.docx")
print("¡Archivo Reporte_OpenSSL.docx generado exitosamente!")