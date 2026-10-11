# Detección y respuesta de amenazas para IoT

## 1. La problemática

Los dispositivos IoT (sensores, cámaras, controladores) se multiplican en casas, escuelas y pequeñas empresas, pero casi siempre se instalan con contraseñas por defecto, sin cifrado y sin nadie que vigile su tráfico. Las organizaciones pequeñas no pueden pagar un SOC ni un SIEM comercial, así que un dispositivo comprometido pasa desapercibido hasta que ya hay daño.

**Pregunta que resolvemos:**

> ¿Cómo detectar y responder de forma automática a ataques contra dispositivos IoT con una solución accesible y de bajo costo?

---

## 2. La solución en una frase

Una **alarma inteligente para dispositivos IoT**: ve lo que pasa, detecta qué ataque es con Machine Learning, avisa en vivo en una app y, en la etapa final, **corta el acceso del dispositivo comprometido** con aprobación de un humano.

### Explicación para alguien que no sabe nada

"Hoy muchos aparatos conectados a internet, como cámaras o sensores, son fáciles de hackear y nadie los vigila. Nosotros hicimos un sistema barato que los vigila, detecta cuando alguien los está atacando, te avisa al instante en una app y bloquea el aparato afectado."

### Explicación técnica 

"Es una plataforma tipo SIEM/SOC de bajo costo. Los eventos de una app vulnerable y de nodos ESP32 se envían por sockets a un backend en la nube, se almacenan en una base de datos y un modelo de ML los clasifica (fuerza bruta, inyección SQL, escaneo, tráfico normal). Una PWA muestra las alertas en tiempo real. Los nodos físicos se autentican con mTLS usando una PKI propia, y cuando se detecta un compromiso el sistema revoca el certificado del nodo, previa aprobación con passkeys."

---

## 3. Qué proyecto vamos a hacer (resumen de la decisión)

| Propuesta | Qué era |
|---|---|---|
| B: App vulnerable + SIEM | Atacamos nuestra propia app y el sistema detecta |
| C: IoT por fases | Nodos ESP32, PKI, mTLS, respuesta automática |

**Por qué esta combinación:** la base no depende de hardware ni de otras personas, así que siempre habrá algo entregable. Lo demás se suma por fases.
---

### El recorrido de un ataque, paso a paso

1. Alguien (nosotros o el jurado) lanza un ataque, por ejemplo fuerza bruta contra el login.
2. La app (o el nodo) genera **eventos/logs** de lo que pasó.
3. Los eventos viajan por **sockets** al backend.
4. El backend los **guarda** en la base de datos.
5. El **modelo de ML** los revisa y dice: "esto es fuerza bruta, confianza 94%".
6. La **PWA** muestra la alerta en segundos.
7. *(Fase 3)* El sistema propone **revocar** el acceso del dispositivo, un humano aprueba con huella o rostro (**passkey**) y el dispositivo queda bloqueado.

---

## 5. Fases 

| Fase | Meses | Qué se construye | Entregable mínimo |
|---|---|---|---|
| **1. Base en la nube** | 1-6 | Juice Shop, backend con sockets, base de datos, ML de clasificación, PWA con alertas | Demo donde atacamos y el dashboard reacciona en vivo |
| **2. Nodos IoT seguros** | 7-12 | Nodos ESP32, PKI propia, mTLS, provisión por QR desde la PWA | Al menos un nodo real conectado de forma segura y enviando eventos |
| **3. Respuesta automática** | 13-18 | Revocación de acceso, aprobación con passkeys, documentación y pruebas finales | Un nodo "comprometido" es bloqueado desde la app |

---

## 8. Roles del equipo

| Rol | Responsable de | Ejemplos de tareas |
|---|---|---|
| **Seguridad, redes y electrónica** | Juice Shop, PKI, mTLS, certificados, firmware ESP32, segmentación de red | Montar la app vulnerable, emitir certificados, programar el ESP32, generar ataques |
| **Backend / Desarrollo** | Base de datos, sockets, arquitectura en la nube, API | Diseñar tablas, recibir eventos en vivo, desplegar servicios, API para la PWA |
| **ML + IHM** | Modelo y dashboard | Etiquetar muestras, entrenar y evaluar el modelo, diseñar la PWA, flujo de passkeys |

---

## 9. Riesgos y cómo los evitamos

| Riesgo | Cómo lo evitamos |
|---|---|
| Falla el hardware el día de la demo | La Fase 1 corre 100% en la nube; el hardware es un extra, no la base. Tener video de respaldo de la demo |
| No alcanzamos a hacer todo | Plan por fases, cada una entregable |
| PKI, mTLS y passkeys son difíciles | Dedicar tiempo de aprendizaje al inicio de cada fase y hacer pruebas pequeñas antes de integrar |
| Pocas muestras para el ML | Las generamos nosotros con herramientas, en cantidad |
| El modelo falla con datos nuevos | Probar con ataques distintos y tener reglas de respaldo |
| Una persona se atrasa o se bloquea | Documentar todo y que al menos dos personas entiendan cada pieza |
| Atacar algo que no es nuestro | Solo nuestro entorno, siempre |

---

## 10. Lo que nos diferencia (opcional, elegir **una**)

El proyecto base usa prácticas vigentes pero conocidas. Para que tenga "algo propio", conviene sumar **una sola** extensión pequeña, con medición real:

- **Mapear las detecciones a MITRE ATT&CK** (la más realista para 3 personas).
- **Probar la robustez del modelo ante evasión** (¿puede un atacante engañarlo?).
- **Detección ligera en el propio dispositivo** (edge ML).
- **Atestación del firmware** del ESP32.


---

## 11. Cómo lo convertimos en valor para el CV

- Repositorio público (sin credenciales ni certificados reales), con README claro y diagrama de arquitectura.
- Métricas reales del modelo documentadas.
- Video corto de la demo.
- Notas de lo que aprendimos y lo que falló.

**Línea para el CV:**

> Diseñé y desarrollé una plataforma de detección y respuesta a amenazas para IoT: ingesta de eventos en tiempo real, clasificación de ataques con ML, autenticación mutua con PKI/mTLS y respuesta automatizada.


---

## 12. Preguntas que nos pueden hacer

**¿Esto ya existe?**
Sí, existen SIEM y soluciones comerciales (Splunk, Wazuh, etc.). Nuestro enfoque es una solución **accesible y de bajo costo** pensada para IoT en organizaciones pequeñas, y construimos las piezas nosotros para entenderlas a fondo.

**¿Por qué una app vulnerable y no una real?**
Porque es legal, segura y nos permite generar ataques controlados y repetibles para entrenar y probar el modelo.

**¿Por qué ML y no solo reglas?**
Las reglas fijas se quedan cortas ante variaciones del ataque. El ML generaliza mejor, aunque dejamos reglas como respaldo.

**¿Qué pasa si el modelo se equivoca?**
Por eso medimos falsos positivos y negativos, y en la respuesta automática un humano aprueba antes de bloquear.

**¿Y si no terminan la Fase 3?**
El proyecto sigue siendo válido: cada fase se entrega por sí sola.

**¿Qué es lo más difícil?**
Hacer que PKI, mTLS y passkeys funcionen en conjunto, y que el modelo funcione con datos que no vio.

---


## 14. Diccionario

### Conceptos del proyecto

| Término | Qué significa en simple |
|---|---|
| **IoT (Internet of Things)** | Aparatos cotidianos conectados a internet: cámaras, sensores, focos, controladores |
| **Nodo** | Cada equipo o dispositivo que forma parte del sistema (un ESP32, un servidor, una instancia en la nube) |
| **ESP32** | Microcontrolador barato con Wi-Fi y Bluetooth, muy usado en IoT |
| **Firmware** | El programa que corre dentro de un dispositivo como el ESP32 |
| **Backend** | El "cerebro" en el servidor: recibe datos, los guarda y ejecuta el modelo |
| **Frontend** | La parte que ve el usuario (en nuestro caso, la PWA) |
| **PWA** | Página web que se instala en el celular o PC como si fuera una app |
| **Dashboard** | Pantalla con gráficas, mapas y alertas para ver todo de un vistazo |
| **Socket / WebSocket** | Conexión en tiempo real que se queda abierta, como una llamada telefónica en vez de mandar cartas |
| **Evento / Log** | Registro de algo que pasó (un login fallido, una petición, una conexión) |
| **Base de datos (BD)** | Donde se guardan los eventos de forma ordenada |
| **API** | Forma en que dos programas se piden datos entre sí |
| **Nube (cloud)** | Servidores de un proveedor (AWS, Azure, etc.) donde corre nuestro backend |
| **SCRUM** | Forma de trabajar en equipo con ciclos cortos llamados sprints |
| **Sprint** | Periodo corto (1-2 semanas) con tareas definidas |
| **Backlog** | Lista de todo lo pendiente por hacer |

### Seguridad

| Término | Qué significa en simple |
|---|---|
| **Ciberseguridad** | Proteger sistemas, redes y datos de ataques |
| **Blue Team** | El equipo que **defiende** y detecta ataques (nosotros) |
| **Red Team** | El equipo que **ataca** para probar las defensas |
| **SIEM** | Sistema que junta y analiza logs de seguridad de muchos lados |
| **SOC** | Centro o equipo que vigila alertas de seguridad |
| **SOAR / XDR / EDR** | Sistemas que además de detectar, **responden** automáticamente a amenazas |
| **Honeypot** | Sistema falso que atrae atacantes para observarlos (lo descartamos como base, pero es parte del contexto) |
| **Amenaza** | Cualquier cosa que pueda dañar un sistema |
| **Vulnerabilidad** | Un punto débil que un atacante puede aprovechar |
| **Fuerza bruta** | Probar contraseñas una y otra vez hasta atinar |
| **Inyección SQL (SQLi)** | Meter código malicioso en un formulario para robar o alterar datos |
| **Escaneo de puertos (port scan)** | Tocar todas las "puertas" de un sistema para ver cuáles están abiertas |
| **Zero trust** | Filosofía de "no confiar en nadie por defecto": todo dispositivo debe demostrar quién es |
| **MITRE ATT&CK** | Catálogo mundial que clasifica las técnicas de los atacantes; es el lenguaje común de los equipos de seguridad |
| **CTF** | Competencias de hackeo ético para practicar |

### Criptografía y acceso

| Término | Qué significa en simple |
|---|---|
| **TLS** | Cifrado que protege la conexión (el candadito del navegador) |
| **mTLS** | TLS donde servidor **y** dispositivo se piden credencial mutuamente antes de hablar |
| **Certificado digital** | Credencial electrónica que prueba la identidad de un dispositivo o servidor |
| **PKI** | Nuestra propia "oficina de credenciales": emite y administra certificados |
| **CA (Autoridad Certificadora)** | La entidad que firma y emite los certificados dentro de la PKI |
| **Revocar** | Cancelar un certificado para que el dispositivo ya no pueda conectarse |
| **Provisión** | Proceso de dar de alta un dispositivo nuevo con su identidad y credenciales |
| **Passkey / WebAuthn / FIDO2** | Inicio de sesión sin contraseña, con huella, rostro o PIN del dispositivo |
| **Atestación** | Que un dispositivo demuestre que su firmware no fue alterado |

### Herramientas

| Término | Qué significa en simple |
|---|---|
| **OWASP Juice Shop** | Tienda web hecha *a propósito* con vulnerabilidades, para practicar ataques de forma legal |
| **hydra** | Herramienta para hacer ataques de fuerza bruta (solo en nuestro entorno) |
| **sqlmap** | Herramienta que automatiza inyecciones SQL |
| **nmap** | Herramienta para escanear puertos y redes |

### Machine Learning

| Término | Qué significa en simple |
|---|---|
| **ML (Machine Learning)** | Programa que aprende de ejemplos para clasificar cosas nuevas |
| **Muestra** | Un ejemplo con su etiqueta (ej. "estos eventos son fuerza bruta") |
| **Etiqueta** | El nombre de la clase de una muestra: `sqli`, `escaneo`, `normal`... |
| **Entrenamiento / Prueba** | Datos con los que el modelo aprende / datos nuevos con los que se evalúa |
| **Árbol de decisión** | Modelo de reglas tipo "si hay más de 50 intentos en 10 s → fuerza bruta". Fácil de explicar |
| **Clustering** | Modelo que agrupa ataques parecidos sin etiquetas previas |
| **Detección de anomalías** | Modelo que aprende lo "normal" y avisa cuando algo se sale de ahí |
| **Precisión** | De las alertas que dio el modelo, cuántas eran correctas |
| **Falso positivo** | Alerta de ataque cuando en realidad era tráfico normal |
| **Falso negativo** | Ataque real que el modelo no detectó |
| **Generalizar** | Que el modelo funcione bien con datos que nunca vio |
| **Evasión** | Que un atacante modifique su ataque para engañar al modelo |
| **Edge ML** | Correr el modelo en el propio dispositivo en lugar de en la nube |

---

## Resumen final

- **Problema:** los dispositivos IoT son fáciles de atacar y nadie los vigila, sobre todo en organizaciones pequeñas.
- **Solución:** una plataforma barata que detecta ataques con ML, avisa en vivo y responde bloqueando el dispositivo comprometido.
- **Cómo:** Fase 1 en la nube (base), Fase 2 con nodos ESP32 seguros (PKI + mTLS), Fase 3 con respuesta automática y passkeys.
- **Garantía:** cada fase se entrega por sí sola, así que siempre hay proyecto.
- **Valor:** mezcla desarrollo, ciberseguridad, redes y electrónica, y es demostrable en un CV.
