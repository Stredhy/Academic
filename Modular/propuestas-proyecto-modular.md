# Propuestas para el proyecto modular (explicadas fácil)

> Este documento explica las 3 ideas de proyecto que estamos considerando, qué significa cada término técnico, cuál conviene más y por qué. No hace falta saber de seguridad para entenderlo.

---

## 1. La idea general (aplica a todas las propuestas)

Imagina una **alarma inteligente para sistemas informáticos**. Funciona así:

1. Hay algo que **recibe ataques** (un señuelo o una app vulnerable a propósito).
2. Todo lo que pasa se manda como **eventos (logs)** a un servidor en la nube, usando **sockets**.
3. Los eventos se **guardan en una base de datos**.
4. Un modelo de **Machine Learning (ML)** los revisa y los clasifica: "esto es fuerza bruta", "esto es inyección SQL", "esto es un escaneo".
5. Una **PWA** (página web que se instala como app) muestra las alertas **en vivo**.

Lo que cambia entre propuestas es **qué es lo que recibe los ataques** y **qué tan lejos llegamos**.

---

## 2. Mini diccionario

| Término | Qué significa en simple |
|---|---|
| **Honeypot** | Un sistema falso que *parece* vulnerable para atraer atacantes. No tiene nada valioso; solo sirve para observar qué hacen. Como una cartera falsa con un rastreador dentro. |
| **Nodo** | Cada equipo o instancia que corre un honeypot (una Raspberry Pi, un ESP32 o un servidor en la nube). |
| **Socket** | Conexión en tiempo real entre dos programas. Como una llamada telefónica que se queda abierta, en vez de mandar cartas una por una. |
| **Backend** | El "cerebro" en el servidor: recibe los datos, los guarda y ejecuta el modelo. |
| **Base de datos (BD)** | Donde se guardan todos los eventos ordenados. |
| **ML (Machine Learning)** | Un programa que aprende de ejemplos para clasificar cosas nuevas. |
| **Árbol de decisión** | Modelo de ML basado en reglas tipo "si hace más de 50 intentos de contraseña en 10 segundos → es fuerza bruta". Fácil de explicar al jurado. |
| **Clustering** | Modelo que agrupa ataques parecidos sin que le digamos las etiquetas antes. |
| **Detección de anomalías** | Modelo que aprende lo "normal" y avisa cuando algo se sale de lo normal. |
| **PWA** | Página web que se puede instalar en el celular o PC como si fuera una app. |
| **SIEM** | Sistema que junta y analiza logs de seguridad de muchos lados. |
| **SOC** | El centro o equipo que vigila alertas de seguridad. |
| **Fuerza bruta** | Probar contraseñas una y otra vez hasta atinar. |
| **Inyección SQL** | Meter código malicioso en un formulario para robar o alterar datos de la base de datos. |
| **Escaneo (port scan)** | Tocar todas las "puertas" de un sistema para ver cuáles están abiertas. |
| **OWASP Juice Shop** | Una tienda web hecha *a propósito* con vulnerabilidades, para practicar ataques de forma legal. |
| **PKI** | Nuestra propia "oficina de credenciales": emite certificados digitales para identificar dispositivos. |
| **mTLS** | Conexión donde servidor **y** dispositivo se piden credencial mutuamente antes de hablar. |
| **Passkey** | Inicio de sesión sin contraseña (huella, rostro o PIN del dispositivo). |

---

## 3. Las propuestas

### Propuesta A: Honeypot distribuido con ML

**En una frase:** varios señuelos repartidos en distintos equipos atraen ataques y un modelo de ML clasifica el comportamiento de los atacantes.

**Cómo funciona:**
- Varios nodos (Raspberry Pi o ESP32) actúan como señuelos.
- Cada intento de ataque se manda por sockets a la nube.
- Se guarda en la base de datos.
- El ML (árbol de decisión o clustering) clasifica qué tipo de atacante es.
- La PWA muestra todo.

**Las 35 muestras:** salen de los ataques que haga el público durante la demo.

**Puntos a favor**
- Muy visual: "nodos distribuidos" se ve profesional.
- Cubre bien el tema de nodos en distintos equipos.

**Puntos en contra**
- Depende de hardware físico (Raspberry/ESP32), que puede fallar el día de la presentación.
- Depende del público para generar las muestras, lo cual es impredecible.

---

### Propuesta B: Detección de ataques a una app web (tipo SIEM/SOC)

**En una frase:** montamos una app vulnerable a propósito, la "atacamos" (o la ataca el jurado) y nuestro sistema detecta y muestra alertas en vivo.

**Cómo funciona:**
- Se monta **OWASP Juice Shop** en nuestro propio entorno.
- Esa app manda sus logs por sockets a nuestro backend.
- Se guardan en la base de datos.
- El ML detecta comportamiento anormal: fuerza bruta, inyección SQL, escaneos.
- La PWA muestra las alertas al instante.

**Las 35+ muestras:** las generamos nosotros antes de la demo con herramientas de ataque (ver sección 6).

**Puntos a favor**
- La demo es muy clara: el jurado ataca → el dashboard reacciona en segundos.
- Todo es software, no depende de hardware.
- Muy bueno para el CV: SIEM, SOC y detección de amenazas son justo lo que piden en vacantes de seguridad.

**Puntos en contra**
- Es menos "IoT" que las otras.
- Menos llamativo en cuanto a redes/dispositivos físicos.

---

### Propuesta C: Plataforma de detección y respuesta para IoT (por fases)

**En una frase:** la versión más ambiciosa. Se construye en 3 fases, de modo que si algo se atrasa, nos quedamos con la fase anterior y el proyecto sigue siendo válido.

| Fase | Qué se construye | Explicación simple |
|---|---|---|
| **1** (mínimo que ya aprueba) | Honeypots en la nube, backend con sockets, base de datos, ML de clasificación, PWA con mapa y alertas | Todo corre en la nube. No depende de hardware físico. |
| **2** | Nodos ESP32 con **mTLS** y **PKI propia**, provisión por **QR** desde la PWA | Cada dispositivo físico tiene su credencial digital. Se agrega escaneando un QR desde la app. |
| **3** | Respuesta automática (revocar acceso) y aprobación con **passkeys** | Si se detecta un ataque, el sistema corta el acceso del dispositivo comprometido, y un humano lo aprueba con huella/rostro. |

**Puntos a favor**
- Es el proyecto más completo e impresionante.
- Cubre redes, seguridad, IoT y criptografía (útil para CCNA).
- Por fases: nadie te rechaza por complejidad y no te la juegas toda al hardware.

**Puntos en contra**
- Requiere más tiempo y alguien con base en redes/criptografía.
- Las fases 2 y 3 pueden no alcanzar a terminarse.

---

## 4. Comparación rápida

| | A: Honeypot distribuido | B: App vulnerable + SIEM | C: IoT por fases |
|---|---|---|---|
| **Dificultad** | Media | Baja-Media | Media-Alta |
| **Riesgo de que falle en la demo** | Medio-Alto (hardware + público) | Bajo | Bajo en fase 1, mayor en fases 2-3 |
| **Qué tan clara es la demo** | Media | Muy clara | Clara |
| **Valor para el CV** | Bueno | Muy bueno (SIEM/SOC) | Excelente |
| **Cubre módulos 2, 3 y 4** | Sí | Sí | Sí |
| **Control sobre las 35 muestras** | Bajo (depende del público) | Alto (las generamos nosotros) | Alto |

---

## 5. Mi sugerencia

### **Empezar con B como base, y usar las fases de C como plan de crecimiento.**

En otras palabras: no elegir entre "B o C". Se combinan.

**Paso 1: Construir la base (equivale a la Fase 1 de C).**
Montamos la app vulnerable (Juice Shop), el backend con sockets, la base de datos, el modelo de ML y la PWA con alertas. Esto ya cubre los módulos 2, 3 y 4 completos y se puede demostrar.

**Paso 2: Si vamos bien de tiempo, agregar nodos ESP32 con mTLS y PKI (Fase 2 de C).**
Esto le da el toque IoT y de redes.

**Paso 3: Si todavía sobra tiempo, agregar respuesta automática y passkeys (Fase 3 de C).**
Es el extra que nos diferencia.

### ¿Por qué esta combinación?

1. **Seguridad ante todo.** El paso 1 no depende de hardware ni del público. Es controlable.
2. **Demo garantizada.** El jurado ataca y ve la alerta en vivo. Eso vende.
3. **Las 35 muestras las controlamos nosotros.** No dependemos de que el público "coopere".
4. **Crece sin riesgo.** Si algo se atrasa, ya tenemos un proyecto sólido entregable. Si todo sale bien, terminamos con algo espectacular.
5. **Buen CV.** SIEM, SOC y detección de amenazas es lo que buscan las vacantes de seguridad; mTLS/PKI suma puntos extra.

---

## 6. Cómo generar las 35+ muestras (para el módulo 4)

Para entrenar el modelo necesitamos ejemplos de ataques y de tráfico normal. Los generamos **contra nuestra propia app** (nunca contra sistemas ajenos):

| Tipo de ataque | Herramienta común | Qué produce en los logs |
|---|---|---|
| Fuerza bruta | `hydra` | Muchos intentos de login fallidos seguidos |
| Inyección SQL | `sqlmap` | Peticiones con texto raro tipo `' OR 1=1 --` |
| Escaneo | `nmap` | Muchas conexiones a puertos distintos en poco tiempo |
| Tráfico normal | Navegar la app a mano | Peticiones normales y espaciadas |

Meta sugerida: unas 10 muestras por tipo de ataque más varias de tráfico normal, hasta pasar de 35. Cada muestra se etiqueta (ej. `fuerza_bruta`, `sqli`, `escaneo`, `normal`) y se usa para entrenar y probar el modelo.

---

## 7. Cómo nos repartimos el trabajo

| Rol | Responsable de | Ejemplos de tareas |
|---|---|---|
| **Seguridad y redes** | Honeypots/app vulnerable, PKI, mTLS, firmware (fases 2-3) | Montar Juice Shop, configurar certificados, programar ESP32 |
| **Backend** | Base de datos, sockets, arquitectura | Diseñar tablas, recibir eventos en vivo, API para la PWA |
| **ML + IHM** | Modelo y dashboard | Generar/etiquetar muestras, entrenar el modelo, diseñar la PWA |

---

## 8. Cómo encaja con los módulos

| Módulo | Qué cubrimos |
|---|---|
| **Módulo 2** | Diseño de la base de datos, metodología SCRUM (sprints, backlog) y estándares de documentación/código |
| **Módulo 3** | Servicios separados en la nube, sockets, comunicación entre nodos/equipos |
| **Módulo 4** | Modelo de ML (clasificación o detección de anomalías) entrenado con las 35+ muestras |

---

## 9. Riesgos y cómo evitarlos

| Riesgo | Cómo lo evitamos |
|---|---|
| Falla el hardware el día de la demo | La fase 1 corre 100% en la nube; el hardware es un extra, no la base |
| No alcanzamos a hacer todo | El proyecto está planeado por fases; cada una es entregable por sí sola |
| Pocas muestras para el ML | Las generamos nosotros con herramientas antes de la demo |
| El modelo falla en vivo con datos nuevos | Probar antes con ataques distintos a los de entrenamiento y tener reglas de respaldo |
| Ataques a sistemas que no son nuestros | Solo atacamos nuestra propia app en nuestro entorno |

---

## 10. Próximos pasos

1. Que el equipo decida: ¿vamos con **B + fases de C**?
2. Repartir roles (sección 7).
3. Armar el backlog y el primer sprint de SCRUM (módulo 2).
4. Montar Juice Shop y el backend mínimo que reciba logs por sockets.
5. Empezar a generar y etiquetar muestras cuanto antes.

---

## Resumen en 30 segundos

- **A** = señuelos distribuidos + ML. Vistoso, pero depende de hardware y del público.
- **B** = app vulnerable + detección en vivo. Seguro, fácil de demostrar, bueno para el CV.
- **C** = plataforma IoT por fases. La más ambiciosa, pero es mejor tomarla como un plan de crecimiento.
- **Recomendación:** empezar con **B** y crecer con las fases de **C**. Así siempre hay proyecto que entregar y, si todo sale bien, algo que destaque.
