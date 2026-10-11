# Reporte Técnico: Práctica 1 - ESP32, LEDs y Botones

**Materia:** Internet de las Cosas (IoT)  
**Plataforma:** Wokwi / ESP32  

---

## Fase 1: Control de Salida Digital Fija (Un solo LED)

* **Funcionamiento del código:**  
  Se utiliza el espacio de nombres `Config` para definir el pin asignado (`PIN_LED_PRINCIPAL` en GPIO25). En la función `setup()`, se declara el terminal como salida digital mediante `pinMode()` y se establece en estado lógico alto constante usando `digitalWrite(..., HIGH)`. Dado que la salida no requiere cambios dinámicos, la función `loop()` permanece sin instrucciones executionales.
* **Aprendizaje clave:**  
  Manejo básico de registros de dirección de pines (GPIO) como salidas digitales estáticas y comprensión del flujo de inicialización en sistemas embebidos.

---

## Fase 2: Concurrencia No Bloqueante (LED Fijo + LED Parpadeante)

* **Funcionamiento del código:**  
  En lugar de suspender la ejecución del procesador utilizando `delay()`, se implementa temporización asíncrona mediante la función `millis()`. El primer LED permanece encendido de forma continua desde el `setup()`. En el bucle principal (`loop()`), se evalúa periódicamente la diferencia entre el tiempo actual y el último cambio de estado (`tiempoActual - tiempoAnterior`). Al alcanzar el umbral de 3000 ms, se invierte la variable de estado y se actualiza el valor del segundo LED en GPIO26.
* **Aprendizaje clave:**  
  Implementación de tareas no bloqueantes para multitarea en microcontroladores, evitando el congelamiento de la CPU y garantizando alta disponibilidad del sistema.

---

## Fase 3: Mapeo de Entradas y Lógica Pull-Up (2 LEDs y 2 Botones)

* **Funcionamiento del código:**  
  Los pines de entrada (GPIO32 y GPIO33) se configuran en modo `INPUT_PULLUP`, activando las resistencias internas conectadas a $V_{CC}$. Esta configuración invierte la lógica digital: el pin lee un estado alto (`HIGH`) en reposo y un estado bajo (`LOW`) al presionar el pulsador (conexión a tierra). La función modular `procesarEntradas()` consulta el estado de las entradas e invierte el valor lógico para activar los LEDs correspondientes (GPIO25 y GPIO26) solo mientras el botón permanezca oprimido.
* **Aprendizaje clave:**  
  Lectura e interpretación de entradas digitales con lógica Pull-Up, acondicionamiento de señales físicas mediante software y diseño modular fuertemente tipado.

---

## Resumen de Arquitectura y Buenas Prácticas

| Criterio | Práctica Tradicional | Implementación Profesional (9no Semestre) |
| :--- | :--- | :--- |
| **Asignación de Pines** | `#define LED 25` | `constexpr uint8_t PIN_LED {25}` en `namespace` |
| **Control de Tiempo** | `delay(3000)` (Bloqueante) | `millis()` (Asíncrono / No bloqueante) |
| **Estructuración** | Lógica masiva dentro de `loop()` | Funciones modulares dedicadas (`procesarEntradas()`) |
| **Documentación** | Sin comentarios o comentarios básicos | Documentación formal de encabezados (estilo Doxygen) |