# Matriz de requerimientos – NutriMaker

| ID | Tipo | Funcionalidad | Requerimiento | Prioridad | Comentarios | ID_Test_Case_Satisfied |
|---|---|---|---|---|---|---|
| RF-01 | Funcional | Login | Validar correo y contraseña; cifrado AES-128 + TLS 1.2. | Alta (sugerida) | Implementado en código (`LoginController`). | Pendiente |
| RF-02 | Funcional | Registro | Alta de usuario con validación de correo y contraseña. | Alta (sugerida) | Implementado (`SignUpController`). | Pendiente |
| RF-03 | Funcional | Almacenamiento de dietas | Listar, crear, exportar, modificar y eliminar dietas. | Alta (sugerida) | Implementado (`DietStorageController`). | Pendiente |
| RF-04 | Funcional | Crear dieta | Generación automática según calorías, objetivos y restricciones. | Alta (sugerida) | Implementado (`CreateDietController`). | Pendiente |
| RF-05 | Funcional | Datos del paciente | Captura de nombre, altura, edad y peso. | Media (sugerida) | Implementado (`PatientFormController`). | Pendiente |
| RF-06 | Funcional | Modificar dieta | Edición de alimentos con generación automática. | Media (sugerida) | Implementado. | Pendiente |
| RF-07 | Funcional | Eliminar dieta | Confirmación y eliminación de dieta. | Media (sugerida) | Implementado. | Pendiente |
| RF-08 | Funcional | Exportar a PDF | Generación y vista previa del PDF de la dieta. | Media (sugerida) | Implementado (`PDFBuilder`). | Pendiente |

> **Nota:** Las prioridades son sugeridas y los identificadores de casos de prueba están pendientes de asignación.
