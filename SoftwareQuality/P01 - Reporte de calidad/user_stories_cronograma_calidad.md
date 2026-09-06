# Plantillas de historias de usuario — Cronograma de calidad de SW

## NutriMaker

### 1. Evaluación inicial y métricos (WK2)

**Como** equipo de calidad de NutriMaker
**Necesito** evaluar el estado actual del proyecto y establecer los métricos a monitorear durante el curso
**Para que** tengamos una línea base clara para medir el progreso de calidad durante el semestre

### Detalles y Supuestos
* Corresponde a WK2 del cronograma de calidad
* Métricos definidos: tasa de defectos, cobertura de pruebas, CSAT, velocidad media, predictibilidad, lead time
* Actividad ya completada

### Criterios de Aceptación

```gherkin
Dado que el equipo revisó el estado actual del código y documentación de NutriMaker
Cuando se define la lista de métricos a monitorear
Entonces quedan documentados los 6 métricos con su fórmula y objetivo ideal
```

---

### 2. Software Architecture Document (SAD)

**Como** equipo de desarrollo de NutriMaker
**Necesito** documentar la arquitectura del sistema en capas
**Para que** el diseño quede como referencia formal para el equipo y para futuras entregas

### Detalles y Supuestos
* Arquitectura actual: Java/JavaFX + Oracle Autonomous DB, en capas (models, controllers, repository, PDFBuilder)
* Dependencia: evaluación inicial completada

### Criterios de Aceptación

```gherkin
Dado el código fuente organizado en capas
Cuando se documenta la arquitectura en el SAD
Entonces el documento describe cada capa, sus responsabilidades y cómo se comunican entre sí
```

---

### 3. Software Design Document (SDD)

**Como** equipo de desarrollo de NutriMaker
**Necesito** documentar el diseño detallado de cada módulo
**Para que** quede claro cómo está construido cada controlador antes de tocarlo o probarlo

### Detalles y Supuestos
* Incluye LoginController, SignUpController, DietStorageController, CreateDietController, PatientFormController, PDFBuilder
* Dependencia: SAD

### Criterios de Aceptación

```gherkin
Dada la arquitectura general documentada en el SAD
Cuando se detalla el diseño de cada módulo funcional
Entonces el SDD describe clases, atributos y métodos principales de cada controlador
```

---

### 4. SW Test Plan

**Como** equipo de calidad de NutriMaker
**Necesito** definir el plan de pruebas de software
**Para que** sepamos qué y cómo probar antes de generar el primer set de tests automatizados

### Detalles y Supuestos
* Actualmente no existe carpeta src/test; este plan incluye definir el entorno con JUnit
* Dependencia: SDD

### Criterios de Aceptación

```gherkin
Dados los requerimientos funcionales de la matriz (RF-01 a RF-08)
Cuando se elabora el Test Plan
Entonces queda definido el alcance, casos de prueba priorizados y la herramienta a usar (JUnit)
```

---

### 5. Test Report

**Como** equipo de calidad de NutriMaker
**Necesito** ejecutar las pruebas definidas y generar el reporte de resultados
**Para que** tengamos evidencia objetiva de qué funcionalidades pasan y cuáles no

### Detalles y Supuestos
* Depende de tener el entorno de pruebas funcionando y el Test Plan aprobado
* Debe incluir gráfica de pastel de total de pruebas y distribución por funcionalidad

### Criterios de Aceptación

```gherkin
Dado un Test Plan aprobado y casos de prueba implementados en JUnit
Cuando se ejecutan las pruebas
Entonces se genera un Test Report con resultados, porcentaje de éxito y gráficas por funcionalidad
```

---

### 6. Dashboard

**Como** equipo de calidad de NutriMaker
**Necesito** crear un dashboard con los métricos de software recabados desde WK2
**Para que** el equipo y el profesor puedan ver el estado de calidad en cualquier momento

### Detalles y Supuestos
* Debe mostrar: defect density, cobertura, CSAT, velocidad, predictibilidad, lead time
* Debe incluir historial por métrico, no solo el valor actual, con semáforos de status

### Criterios de Aceptación

```gherkin
Dados los datos recabados desde WK2
Cuando se construye el dashboard
Entonces se muestra una pantalla con status en semáforo e historial de cada métrico
```

---

### 7. Monitoreo semanal

**Como** equipo de calidad de NutriMaker
**Necesito** actualizar los métricos del dashboard cada semana
**Para que** detectemos desviaciones a tiempo y podamos ajustar el proceso antes de la entrega final

### Detalles y Supuestos
* Actividad continua desde que el dashboard está listo hasta el fin del curso
* Dependencia: dashboard creado

### Criterios de Aceptación

```gherkin
Dado el dashboard ya configurado
Cuando llega el corte semanal
Entonces se actualizan los 6 métricos con los datos más recientes del sprint/semana
```

---

## Mis Trapitos

### 0. Refactorización y modularización (prerequisito)

**Como** equipo de desarrollo de Mis Trapitos
**Necesito** refactorizar el archivo único de Python en módulos separados
**Para que** sea posible integrar pruebas automatizadas y reducir la deuda técnica actual

### Detalles y Supuestos
* Código actual: un solo archivo de 1,658 líneas (87.5 KB), sin modularización
* Es prerequisito para el SAD, el SDD y las pruebas con pytest
* Dependencia: evaluación inicial

### Criterios de Aceptación

```gherkin
Dado el código actual en un solo archivo monolítico
Cuando se separa en módulos (productos, ventas, inventario, clientes, proveedores, reportes)
Entonces cada módulo puede importarse y probarse de forma independiente
```

---

### 1. Evaluación inicial y métricos (WK2)

**Como** equipo de calidad de Mis Trapitos
**Necesito** evaluar el estado actual del proyecto y establecer los métricos a monitorear durante el curso
**Para que** tengamos una línea base clara para medir el progreso de calidad durante el semestre

### Detalles y Supuestos
* Corresponde a WK2 del cronograma de calidad
* Documentación base ya existe en estándar IEEE-830; el código es lo que falta modularizar
* Actividad ya completada

### Criterios de Aceptación

```gherkin
Dado que el equipo revisó el estado actual del código y documentación de Mis Trapitos
Cuando se define la lista de métricos a monitorear
Entonces quedan documentados los 6 métricos con su fórmula y objetivo ideal
```

---

### 2. Software Architecture Document (SAD)

**Como** equipo de desarrollo de Mis Trapitos
**Necesito** actualizar el documento de arquitectura tras la modularización
**Para que** el diseño real del sistema quede reflejado, no el archivo monolítico original

### Detalles y Supuestos
* Debe describir los módulos resultantes del refactor
* Dependencia: refactorización completada

### Criterios de Aceptación

```gherkin
Dado el código ya modularizado
Cuando se documenta la arquitectura en el SAD
Entonces el documento describe cada módulo, sus responsabilidades y su relación con la base de datos SQLite
```

---

### 3. Software Design Document (SDD)

**Como** equipo de desarrollo de Mis Trapitos
**Necesito** actualizar el diseño detallado de cada módulo
**Para que** quede claro cómo está construida cada función (save_product, register_sale, etc.)

### Detalles y Supuestos
* Cubre los 26 requerimientos funcionales de la matriz (productos, ventas, inventario, clientes, proveedores, reportes)
* Dependencia: SAD

### Criterios de Aceptación

```gherkin
Dada la arquitectura modular documentada en el SAD
Cuando se detalla el diseño de cada módulo funcional
Entonces el SDD describe las funciones principales y su relación con cada RF de la matriz
```

---

### 4. SW Test Plan

**Como** equipo de calidad de Mis Trapitos
**Necesito** definir el plan de pruebas e integrar pytest al proyecto
**Para que** podamos verificar automáticamente lo que hoy solo se valida manualmente

### Detalles y Supuestos
* Hoy la verificación es manual (matriz de rastreabilidad sin pruebas ejecutables)
* Dependencia: refactorización + SDD

### Criterios de Aceptación

```gherkin
Dados los 26 requerimientos funcionales ya modularizados
Cuando se elabora el Test Plan e integra pytest
Entonces queda definido el alcance, casos de prueba priorizados por módulo y la herramienta a usar
```

---

### 5. Test Report

**Como** equipo de calidad de Mis Trapitos
**Necesito** ejecutar las pruebas con pytest y generar el reporte de resultados
**Para que** tengamos evidencia objetiva de qué funcionalidades pasan y cuáles no

### Detalles y Supuestos
* Primera ejecución de pruebas automatizadas del proyecto
* Debe incluir gráfica de pastel de total de pruebas y distribución por funcionalidad (productos, ventas, reportes, etc.)

### Criterios de Aceptación

```gherkin
Dado un Test Plan aprobado y casos de prueba implementados en pytest
Cuando se ejecutan las pruebas
Entonces se genera un Test Report con resultados, porcentaje de éxito y gráficas por funcionalidad
```

---

### 6. Dashboard

**Como** equipo de calidad de Mis Trapitos
**Necesito** crear un dashboard con los métricos de software recabados desde WK2
**Para que** el equipo y el profesor puedan ver el estado de calidad en cualquier momento

### Detalles y Supuestos
* Debe mostrar: defect density, cobertura, CSAT, velocidad, predictibilidad, lead time
* Debe incluir historial por métrico, no solo el valor actual, con semáforos de status

### Criterios de Aceptación

```gherkin
Dados los datos recabados desde WK2
Cuando se construye el dashboard
Entonces se muestra una pantalla con status en semáforo e historial de cada métrico
```

---

### 7. Monitoreo semanal

**Como** equipo de calidad de Mis Trapitos
**Necesito** actualizar los métricos del dashboard cada semana
**Para que** detectemos desviaciones a tiempo y podamos ajustar el proceso antes de la entrega final

### Detalles y Supuestos
* Actividad continua desde que el dashboard está listo hasta el fin del curso
* Dependencia: dashboard creado

### Criterios de Aceptación

```gherkin
Dado el dashboard ya configurado
Cuando llega el corte semanal
Entonces se actualizan los 6 métricos con los datos más recientes del sprint/semana
```
