# Reconocimiento y Escaneo de la Infraestructura

> **Investigación académica:** fundamentos, técnicas, herramientas y aplicaciones en ciberseguridad.  
> **Base de la práctica:** Nmap, Recon-ng y Argus.  
> **Nessus:** referencia conceptual; actividad aún no realizada.  
> **Fecha:** octubre de 2026.

---

## Índice

- [1. Introducción Y Propósito Del Estudio](#1-introduccion-y-proposito-del-estudio)
- [2. Alcance, Autorización Y Metodología](#2-alcance-autorizacion-y-metodologia)
- [3. Fundamentos De Red Necesarios Para Interpretar Un Escaneo](#3-fundamentos-de-red-necesarios-para-interpretar-un-escaneo)
- [4. Reconocimiento Local: Interfaces, Rutas Y Contexto](#4-reconocimiento-local-interfaces-rutas-y-contexto)
- [5. Reconocimiento Pasivo Y Activo](#5-reconocimiento-pasivo-y-activo)
- [6. Descubrimiento De Hosts Con Nmap](#6-descubrimiento-de-hosts-con-nmap)
- [8. Escaneo De Puertos Tcp](#8-escaneo-de-puertos-tcp)
- [9. Escaneo Udp Y Particularidades De Snmp](#9-escaneo-udp-y-particularidades-de-snmp)
- [10. Detección De Servicios, Versiones Y Sistemas Operativos](#10-deteccion-de-servicios-versiones-y-sistemas-operativos)
- [11. Enumeración Smb Y Servicios Compartidos](#11-enumeracion-smb-y-servicios-compartidos)
- [12. Mysql, Nse Y Alcance De Los Scripts](#12-mysql-nse-y-alcance-de-los-scripts)
- [13. Opciones De Paquetes, Fragmentación Y Observabilidad](#13-opciones-de-paquetes-fragmentacion-y-observabilidad)
- [14. Salida De Resultados Y Evidencia Técnica](#14-salida-de-resultados-y-evidencia-tecnica)
- [15. Reconocimiento Web Y Archivos Públicos](#15-reconocimiento-web-y-archivos-publicos)
- [16. Recon-Ng: Organización Del Reconocimiento Osint](#16-recon-ng-organizacion-del-reconocimiento-osint)
- [17. Argus: Entorno Modular Y Límites De La Evidencia](#17-argus-entorno-modular-y-limites-de-la-evidencia)
- [18. Nessus Como Herramienta Complementaria](#18-nessus-como-herramienta-complementaria)
- [19. Interpretación, Validación Y Priorización De Hallazgos](#19-interpretacion-validacion-y-priorizacion-de-hallazgos)
- [20. Aplicaciones Defensivas Del Escaneo De Infraestructura](#20-aplicaciones-defensivas-del-escaneo-de-infraestructura)
- [21. Limitaciones, Falsos Resultados Y Consideraciones Éticas](#21-limitaciones-falsos-resultados-y-consideraciones-eticas)
- [22. Propuesta De Secuencia Didáctica Para La Práctica](#22-propuesta-de-secuencia-didactica-para-la-practica)
- [23. Discusión Integradora: Qué Se Puede Y Qué No Se Puede Concluir](#23-discusion-integradora-que-se-puede-y-que-no-se-puede-concluir)
- [24. Conclusiones](#24-conclusiones)

---

> **Alcance y evidencia:** Los archivos entregados documentan comandos y procedimientos, pero no resultados completos de ejecución. Por ello, el trabajo distingue capacidades técnicas de hallazgos comprobados. Las pruebas deben realizarse únicamente en sistemas autorizados.

## 1. Introducción Y Propósito Del Estudio

La infraestructura informática está formada por equipos, interfaces, direcciones, servicios, protocolos, aplicaciones y relaciones de comunicación. Su seguridad depende tanto de los mecanismos de protección como de la capacidad para reconocer qué recursos existen y cómo se encuentran expuestos. Por esta razón, el reconocimiento y el escaneo constituyen actividades fundamentales de una evaluación técnica: permiten pasar de una percepción general de la red a un inventario contrastable de activos y puntos de entrada. No equivalen por sí mismos a demostrar una intrusión ni a confirmar una vulnerabilidad; su valor está en generar evidencias que orienten revisiones posteriores.

Este trabajo analiza las técnicas documentadas en los tres archivos entregados para la práctica: reconocimiento y escaneo de infraestructura con Nmap, uso de Recon-ng y preparación y ejecución de módulos en Argus. El enfoque se amplía mediante bibliografía técnica de Nmap, NIST, OWASP, Recon-ng y Tenable. El contenido diferencia las instrucciones registradas de los resultados realmente observados: los archivos muestran comandos y secuencias de trabajo, pero no incluyen salidas completas que permitan afirmar cuántos equipos estaban activos, qué puertos se encontraron abiertos o qué fallas fueron confirmadas. Esta distinción evita presentar posibilidades técnicas como hallazgos experimentales.

El objetivo general consiste en explicar qué información puede obtenerse durante una evaluación de infraestructura, cómo se relacionan las herramientas utilizadas y cuáles son las precauciones metodológicas para interpretar los resultados. Entre los objetivos específicos están describir el descubrimiento de hosts, examinar la exploración TCP y UDP, explicar la detección de versiones y sistemas operativos, interpretar la enumeración SMB y MySQL, comprender el reconocimiento de fuentes abiertas y señalar el papel complementario de los analizadores de vulnerabilidades. Se considera siempre un laboratorio propio o un entorno expresamente autorizado. [1][2]

---

## 2. Alcance, Autorización Y Metodología

Una evaluación confiable comienza antes del primer paquete enviado. Debe establecerse quién autoriza la actividad, qué direcciones y dominios pertenecen al alcance, cuáles son los horarios permitidos, qué técnicas quedan excluidas y cómo se comunicarán los incidentes. Un mismo comando puede ser razonable en una máquina virtual de laboratorio e inapropiado en un sistema productivo sensible. El permiso para consultar información pública tampoco implica permiso para probar contraseñas, ejecutar scripts intrusivos o sobrecargar servidores. El marco NIST SP 800-115 insiste en planificar, ejecutar, analizar y documentar las evaluaciones de seguridad. [1]

Conviene separar cinco momentos. Primero se define el alcance y se revisan los riesgos; después se recolecta información pasiva; posteriormente se confirma la presencia de equipos mediante pruebas activas controladas; en una cuarta etapa se examinan puertos, servicios y configuraciones; finalmente se validan hallazgos, se establecen prioridades y se redacta el informe. Este orden no es rígido: un descubrimiento puede obligar a revisar el inventario o a reducir el ritmo de escaneo. La secuencia debe ser repetible y registrar fecha, origen de las pruebas, destino, parámetros, versiones de herramientas y evidencias preservadas.

En los materiales proporcionados aparecen objetivos de laboratorio en el segmento privado 192.168.147.0/24 y referencias a dominios y direcciones públicas. Para el estudio se usan marcadores <IP>, <RED/CIDR> y <DOMINIO> con la finalidad de enseñar la sintaxis sin promover el sondeo de sistemas ajenos. El archivo base ya distingue comandos válidos, duplicados y errores de escritura. Es importante conservar esa depuración como parte de la trazabilidad: un historial de terminal refleja intentos de ejecución, no necesariamente pruebas completadas con éxito.

---

## 3. Fundamentos De Red Necesarios Para Interpretar Un Escaneo

El modelo TCP/IP permite comprender por qué distintos tipos de escaneo producen respuestas diferentes. En la capa de enlace se encuentran las direcciones MAC y mecanismos como ARP; en la capa de red se utilizan direcciones IP y mensajes ICMP; en la capa de transporte aparecen TCP y UDP; sobre ellos funcionan protocolos de aplicación como HTTP, SSH, SMB, DNS o SNMP. Un resultado de Nmap no debe interpretarse aisladamente: la ruta de comunicación, los filtros y el protocolo examinado condicionan la respuesta. La ausencia de respuesta no demuestra automáticamente la ausencia de un equipo.

Las direcciones IPv4 identifican interfaces dentro de una estructura de red, y la notación CIDR indica cuántos bits forman el prefijo. Por ejemplo, /24 corresponde habitualmente a una subred con 256 direcciones posibles, aunque no todas se asignan a equipos finales. Una dirección privada es apropiada para prácticas internas; una dirección pública puede estar administrada por terceros y exige autorización específica. IPv6 introduce un espacio de direcciones mucho mayor y requiere herramientas y filtros compatibles; el indicador -6 de Nmap cambia el contexto del análisis y no debe confundirse con una técnica de descubrimiento por sí sola.

Un puerto lógico permite distinguir servicios que comparten una dirección IP. TCP establece conexiones con intercambio de señales y estados; UDP no utiliza el mismo mecanismo de establecimiento. Por ello, el escaneo TCP suele producir respuestas más concluyentes que algunas exploraciones UDP. La asociación tradicional entre número de puerto y servicio es una pista, no una prueba: una aplicación puede escuchar en un puerto alternativo, un proxy puede mediar la conexión y un firewall puede responder en nombre de otro dispositivo. [2][3]

---

## 4. Reconocimiento Local: Interfaces, Rutas Y Contexto

Antes de explorar otra máquina conviene conocer la propia. Los comandos ip a e ip address, presentes en el material, muestran interfaces, direcciones asignadas y estados relevantes para identificar desde dónde saldrán las sondas. Este paso permite detectar adaptadores virtuales, interfaces desconectadas o direcciones de subred que podrían llevar a elegir un objetivo equivocado. No se trata de un escaneo remoto, sino de una verificación de contexto. En laboratorios con máquinas virtuales, la configuración de NAT, puente o red interna modifica radicalmente qué dispositivos pueden verse entre sí.

La información local debe complementarse con el conocimiento de la puerta de enlace, las tablas de rutas y los filtros del host. Aunque esos comandos complementarios no figuren en los TXT, conceptualmente explican por qué una sonda puede tomar una ruta inesperada. También resulta esencial diferenciar la IP de origen observada por la herramienta de la IP pública vista desde un servidor externo: traducción de direcciones, túneles y VPN pueden producir diferencias. Registrar esta información evita conclusiones erróneas sobre la conectividad y ayuda a reproducir las pruebas.

La práctica también menciona nslookup, empleado para resolver nombres y consultar registros DNS. Un dominio puede asociarse a varias direcciones, y la respuesta puede cambiar según el servidor consultado, la región o el momento. Los registros DNS no constituyen un inventario completo de infraestructura: ciertos equipos carecen de nombres públicos y otros nombres apuntan a redes de distribución de contenido. Por ello, DNS sirve como fuente inicial que debe cruzarse con evidencia adicional antes de atribuir un host a una organización.

---

## 5. Reconocimiento Pasivo Y Activo

El reconocimiento pasivo aprovecha fuentes existentes sin enviar necesariamente pruebas directas a los sistemas examinados. Entre sus fuentes se encuentran buscadores, registros de dominio, certificados públicos, información corporativa y servicios de inteligencia de infraestructura. Su principal ventaja es que puede orientar el alcance y reducir el tráfico generado sobre los objetivos. Sin embargo, los datos pueden estar desactualizados, contener errores o corresponder a proveedores externos. La procedencia y fecha de cada registro son tan importantes como su contenido. [4][5]

El reconocimiento activo interactúa con el objetivo o con componentes de su red. Un descubrimiento ARP, una sonda TCP o una petición HTTP generan señales que pueden ser registradas por los sistemas de defensa. A cambio, permiten verificar estados actuales, aunque siempre condicionados por filtrado, latencia y disponibilidad. No debe equipararse «activo» con «agresivo»: la intensidad depende de la frecuencia, amplitud, tipo de comprobación y sensibilidad del servicio. La práctica combina ambas perspectivas: Recon-ng organiza fuentes abiertas y Nmap realiza comprobaciones directas.

La comparación entre ambos enfoques debe servir para mejorar la precisión. Si un certificado revela un subdominio, se registra como candidato; si una resolución DNS lo asocia a una IP, se añade contexto; si una prueba autorizada confirma respuesta, se clasifica como activo observable. En ningún punto basta una sola señal para atribuir propiedad, exposición o vulnerabilidad. Esta manera gradual de trabajar ayuda a construir un mapa útil sin convertir cada dato aislado en una conclusión exagerada.

---

## 6. Descubrimiento De Hosts Con Nmap

El descubrimiento de hosts responde a una pregunta inicial: ¿qué direcciones parecen corresponder a sistemas disponibles? El archivo de práctica incluye nmap -sn <RED/CIDR>, que busca identificar equipos sin realizar el escaneo habitual de puertos. También documenta la forma antigua -sP, hoy reemplazada por -sn. Un host puede no contestar a una sonda y aun así estar funcionando, por ejemplo porque su firewall bloquea cierto protocolo. Por tanto, el listado obtenido representa equipos detectados mediante los métodos usados, no necesariamente todos los existentes. [2][3]

En redes IPv4 locales, ARP resulta especialmente relevante. La opción -PR solicita descubrimiento ARP cuando se aplica en condiciones compatibles con la red de enlace. Su utilidad proviene de que un dispositivo local necesita resolver direcciones físicas para comunicarse. No obstante, routers y límites de segmento impiden tratar ARP como una técnica universal para Internet. La ubicación del equipo que ejecuta Nmap determina qué puede descubrirse por este método.

El historial también incluye variantes con -PS, -PY, -PM y -PU53. Estas opciones se relacionan respectivamente con sondas TCP SYN, SCTP INIT, ICMP address mask y UDP hacia el puerto indicado. Son caminos distintos para observar señales de presencia, no cuatro formas idénticas de «hacer ping». Algunos equipos responderán a un método y no a otro. La selección debe ajustarse al protocolo disponible, la autorización y las características del entorno, sin asumir que una respuesta negativa constituye evidencia definitiva de inactividad.

Un procedimiento educativo puede comenzar con un segmento de laboratorio pequeño, registrar los hosts detectados y contrastar la lista con las máquinas virtuales encendidas. Si faltan dispositivos conocidos, se revisan la topología y las reglas de filtrado antes de concluir que la herramienta falló. El análisis debe documentar tanto coincidencias como discrepancias. Así se aprende que el descubrimiento es un proceso de inferencia basado en respuestas observables y no un mecanismo infalible de inventariado.

7. RUTAS, TRACEROUTE Y EXPLORACIÓN IPv6
---------------------------------------

La opción --traceroute, utilizada en el material junto con -sn, busca reconstruir los saltos intermedios que responden durante el camino hacia un destino. Su valor consiste en aportar indicios de topología, encaminamiento y puntos donde cambia la visibilidad. No todos los routers contestan ni todas las rutas son simétricas. Un salto ausente no demuestra que la conexión se haya interrumpido: algunos dispositivos simplemente no emiten las respuestas esperadas. Los resultados pueden variar entre momentos debido al balanceo de carga o a cambios en la red.

En IPv6, la opción nmap -6 <DOMINIO> permite explorar direcciones de esa familia cuando existen resolución y conectividad apropiadas. La enorme cantidad de direcciones posibles impide trasladar sin ajustes ciertas prácticas de barrido masivo de IPv4. Es más razonable partir de direcciones conocidas, registros DNS y activos expresamente incluidos en el alcance. Además, una organización puede proteger de manera diferente IPv4 e IPv6, creando exposiciones asimétricas que deben revisarse por separado.

Desde la perspectiva defensiva, documentar rutas y familias de direcciones ayuda a identificar segmentos no previstos, servicios accesibles por una sola pila y diferencias entre políticas de filtrado. Ningún resultado de traceroute revela por sí mismo el diseño físico completo: túneles, NAT, enlaces redundantes y equipos que no responden pueden ocultar parte de la estructura. Por eso se recomienda complementar los hallazgos con diagramas y registros administrativos cuando estén disponibles.

### **Técnicas registradas en la práctica**

- **`nmap -sn <RED/CIDR>`** — Descubrimiento sin escaneo convencional de puertos.
- **`nmap -PR <RED/CIDR>`** — Sondeo ARP en la red local.
- **`nmap -sn -PS <IP>`** — Descubrimiento mediante TCP SYN.
- **`nmap -sn -PU53 <IP>`** — Sondeo UDP hacia el puerto 53.

---

## 8. Escaneo De Puertos Tcp

El escaneo de puertos pretende clasificar la accesibilidad de puntos de comunicación en un host. En la práctica aparecen nmap <IP>, nmap <RED/CIDR>, nmap -p 1-500 <IP> y consultas de puertos concretos como 135 y 139. El escaneo predeterminado de Nmap no significa «todos los puertos»: emplea una selección habitual, salvo que se especifique otro conjunto. Examinar un rango limitado mejora el control del trabajo, pero puede dejar fuera servicios ubicados en números no incluidos. [2][3]

Los estados informados por Nmap deben leerse con cuidado. «open» indica que se detectó un servicio aceptando la modalidad de comunicación comprobada; «closed» indica que el puerto resulta accesible pero no se observa un servicio escuchando; «filtered» expresa que las respuestas no permiten establecer el estado por efecto probable de filtrado. Existen además estados ambiguos como open|filtered y otros específicos de ciertas técnicas. No es correcto traducir «puerto abierto» como «equipo vulnerable»: un servicio puede estar correctamente configurado y actualizado.

La opción -sS realiza un escaneo TCP SYN, y el archivo muestra su uso en un rango con exclusión de un puerto mediante --exclude-ports. Esta técnica interpreta respuestas al inicio del establecimiento TCP, sin que ello garantice invisibilidad frente a sistemas de detección. La exclusión de puertos puede obedecer a restricciones del laboratorio o a la necesidad de evitar servicios sensibles. La elección del rango y del tipo de escaneo debe justificarse en el informe, pues afecta la cobertura y la posibilidad de comparar resultados.

Los puertos 135 y 139, asociados frecuentemente con servicios de Windows y NetBIOS, ilustran por qué conviene interpretar las pistas en contexto. Una respuesta en uno de ellos puede motivar una revisión de SMB y de los servicios expuestos, pero no confirma por sí sola que existan recursos compartidos inseguros. El puerto asociado a SSH también puede consultarse por nombre con -p ssh. Para una evaluación defensiva, la pregunta principal no es solo si un puerto está abierto, sino si ese servicio debe ser accesible desde el segmento probado.

### **Opciones de escaneo TCP documentadas**

- **`nmap <IP>`** — Escaneo de puertos predeterminado.
- **`nmap -p 1-500 <IP>`** — Rango de puertos definido.
- **`nmap -sS -p 100-500 <IP>`** — Escaneo SYN sobre un rango.

---

## 9. Escaneo Udp Y Particularidades De Snmp

UDP presenta dificultades de interpretación distintas de TCP. El archivo incluye nmap -sU -p 161 <IP>, una comprobación orientada al puerto habitualmente utilizado por SNMP. Como UDP no establece conexiones con un intercambio equivalente al de TCP, una ausencia de respuesta puede deberse a que el puerto está abierto, a filtrado o a que la aplicación no responde a la carga enviada. Nmap utiliza respuestas de red y sondas específicas cuando dispone de ellas para reducir la incertidumbre. [3]

SNMP se emplea para observar y administrar dispositivos de red, como switches, routers, impresoras y otros sistemas. Su presencia puede ser legítima y útil para operaciones, pero la exposición innecesaria o configuraciones débiles pueden divulgar información sobre interfaces y equipos. El escaneo inicial solo indica un estado probable del puerto; la revisión de versiones, permisos y autenticación pertenece a una etapa posterior y debe ejecutarse bajo alcance autorizado.

Un informe serio debe reflejar los límites de la evidencia UDP. Es preferible registrar «no se pudo distinguir entre abierto y filtrado» que afirmar un resultado definitivo sin respaldo. Asimismo, las comprobaciones UDP pueden consumir más tiempo que un barrido TCP y deben planificarse para no afectar equipos con recursos limitados. Comparar resultados con configuraciones de firewall y con inventarios de servicios internos puede explicar discrepancias sin recurrir a hipótesis de compromiso.

---

## 10. Detección De Servicios, Versiones Y Sistemas Operativos

La opción -sV aparece repetidamente en la práctica y se orienta a reconocer qué software responde en los puertos detectados. Nmap envía sondas adecuadas y compara las respuestas con patrones conocidos. El resultado puede incluir nombre de servicio, producto y versión aproximada. La precisión depende de la respuesta del servidor, de intermediarios y de la base de firmas utilizada. Una versión anunciada en un banner puede estar modificada, ocultada o no corresponder exactamente al paquete instalado. [2]

El parámetro --version-trace muestra detalles del proceso de identificación y sirve como recurso didáctico para entender por qué se asigna determinada etiqueta. No debería utilizarse para confundir una conjetura con una certeza: la identificación de servicios puede requerir validación administrativa. Desde la perspectiva de seguridad, conocer versiones ayuda a priorizar revisiones de actualización y soporte, pero una versión aparentemente antigua no prueba que sea vulnerable, pues puede contener parches retroportados por el proveedor.

La opción -O intenta inferir el sistema operativo mediante características de la pila de red; -v aumenta el detalle mostrado. El resultado suele expresarse con estimaciones y grados de coincidencia. Dispositivos de filtrado, virtualización y configuraciones de red pueden reducir la fiabilidad. La mejor práctica consiste en reportar «sistema operativo estimado» cuando no existe verificación adicional. En la práctica, estas opciones complementan el reconocimiento de servicios al aportar un perfil técnico del host, no una identificación infalible.

La utilidad administrativa de esta fase es considerable: permite contrastar el inventario oficial con lo realmente observable, detectar servicios olvidados y advertir inconsistencias entre políticas y despliegues. También ayuda a preparar ventanas de mantenimiento, segmentar equipos por criticidad y planificar comprobaciones posteriores. Su alcance, sin embargo, sigue limitado a las respuestas accesibles desde el punto de observación.

### **Indicadores de identificación**

- **`-sV`** — Detección de servicio y versión.
- **`-O`** — Estimación de sistema operativo.
- **`--version-trace`** — Detalle del proceso de detección de versiones.

---

## 11. Enumeración Smb Y Servicios Compartidos

La enumeración profundiza sobre un servicio ya identificado. En el archivo se documentan scripts de Nmap como smb-os-discovery.nse, smb-enum-shares.nse, smb-enum-users.nse y smb-security-mode. Su finalidad general es obtener información acerca de características del sistema, recursos compartidos, usuarios observables y parámetros de seguridad SMB. Estos resultados pueden ayudar a verificar si una organización expone más información de la necesaria. La disponibilidad de datos depende de versiones del protocolo, autenticación, permisos y políticas de acceso. [2]

SMB permite compartir archivos, impresoras y otros recursos, especialmente en entornos Windows. Su presencia no constituye una falla. El riesgo aparece cuando se exponen servicios fuera de los segmentos previstos, se mantienen configuraciones incompatibles con la política o se otorgan permisos excesivos. Un recurso compartido listado no significa que su contenido sea accesible sin autorización. Del mismo modo, obtener nombres de cuentas no equivale a conocer credenciales. El analista debe distinguir identificación de activos, enumeración y pruebas de autenticación.

El script smb-security-mode puede aportar señales sobre mecanismos de protección negociados por SMB. La interpretación exige contexto: no basta etiquetar un ajuste como inseguro sin revisar requisitos, versiones y controles compensatorios. El TXT de base también registra comandos smb-brute, pero los excluye del alcance principal porque realizan intentos de autenticación. En este resumen se mencionan solo para aclarar la frontera metodológica: un reconocimiento autorizado no concede automáticamente permiso para realizar ataques de diccionario o fuerza bruta.

Los hallazgos útiles para un reporte incluyen qué hosts exponen SMB, desde qué red son accesibles, qué configuraciones se pudieron observar y qué validaciones requieren intervención del administrador. Las recomendaciones defensivas suelen orientarse a segmentación, mínimos privilegios, reducción de exposición y mantenimiento del protocolo, siempre sujetas a la arquitectura real de la organización.

### **Scripts SMB estudiados**

- **`smb-os-discovery`** — Información de sistema y dominio.
- **`smb-enum-shares`** — Recursos compartidos.
- **`smb-enum-users`** — Enumeración de usuarios.
- **`smb-security-mode`** — Configuración de seguridad SMB.

---

## 12. Mysql, Nse Y Alcance De Los Scripts

La práctica incluye nmap -f --script "mysql-*" -p 3306 <IP>, que selecciona una familia de scripts relacionada con MySQL. Esta expresión no representa una sola comprobación: puede abarcar scripts con comportamientos diferentes, incluidos algunos que van más allá del reconocimiento básico. Por ello, antes de utilizar comodines se debe revisar qué scripts se ejecutarán, sus categorías y sus posibles efectos. La presencia del puerto 3306 sugiere un servicio asociado con bases de datos, pero su identificación real requiere observar la respuesta y contrastarla con la configuración autorizada. [2]

Nmap Scripting Engine, conocido como NSE, amplía las capacidades del escáner mediante scripts que automatizan tareas de descubrimiento, enumeración y evaluación. En los materiales aparecen --script safe y --script auth. La categoría safe expresa una clasificación del proyecto, no una garantía absoluta de ausencia de efectos; auth agrupa comprobaciones vinculadas a autenticación y puede incluir acciones que requieren una autorización más específica. La selección responsable de scripts forma parte de la planificación técnica.

Los scripts pueden ser útiles para transformar una observación genérica —por ejemplo, un servicio aparentemente disponible— en una descripción más concreta de la configuración. Sin embargo, sus resultados dependen de versiones, permisos y condiciones de red. Un error de script no demuestra necesariamente que el servicio sea inexistente o seguro. Es aconsejable conservar la salida, identificar el nombre exacto del script y separar los resultados confirmados de los mensajes de error o las inferencias.

El historial original también contiene ejecuciones de --script vuln y otras comprobaciones orientadas a vulnerabilidades. El TXT depurado las dejó fuera de la categoría principal, lo que ofrece una oportunidad didáctica para diferenciar descubrimiento, enumeración y análisis de fallas. Son fases relacionadas, pero con objetivos, impactos y requisitos de autorización diferentes.

---

## 13. Opciones De Paquetes, Fragmentación Y Observabilidad

Los comandos -f, --mtu 8, -g 80 y --data-length 5 aparecen en el material de Nmap. Estas opciones modifican aspectos de las sondas, como la fragmentación IPv4, el puerto de origen o la incorporación de datos adicionales. Desde el punto de vista académico permiten estudiar cómo la forma de un paquete influye en su tránsito, registro e interpretación. No son requisitos normales de un inventario básico y no deben utilizarse como sustitutos de una metodología de escaneo bien definida. [2]

La fragmentación puede interactuar con firewalls, sistemas de detección y mecanismos de reensamblado. Su comportamiento depende del sistema operativo, del enlace y de los dispositivos intermedios; en determinadas redes puede ocasionar pérdida de paquetes o resultados difíciles de interpretar. Cambiar el puerto de origen tampoco concede privilegios ni garantiza atravesar filtros. Los controles modernos pueden inspeccionar conexiones completas y aplicar reglas que no dependen únicamente de ese número.

En un laboratorio, el valor de estas opciones está en comparar trazas y comprender por qué dos pruebas nominalmente parecidas producen resultados diferentes. Para un informe de seguridad se debe describir el propósito de la variación, el efecto observado y las limitaciones, evitando afirmar que una técnica «evade» controles si no existen evidencias. La prioridad operativa es obtener mediciones reproducibles con el menor impacto razonable sobre la infraestructura.

---

## 14. Salida De Resultados Y Evidencia Técnica

La práctica utiliza -oN output.txt para guardar resultados legibles y -oX output.xml para generar XML. La extensión del nombre no determina el formato: un archivo llamado .xml creado con -oN seguiría conteniendo texto normal. Esta distinción, visible en el historial original, es importante para evitar fallas al procesar resultados automáticamente. Un reporte bien elaborado conserva el comando exacto, el momento de ejecución, la versión de la herramienta y el archivo original sin modificaciones. [2]

Los formatos estructurados facilitan comparar escaneos sucesivos, correlacionar hosts y producir indicadores. Sin embargo, una comparación automática puede confundir cambios de red con cambios de seguridad. Si un puerto deja de responder, quizá se cerró el servicio, cambió el firewall, se apagó el equipo o falló la conectividad. Por eso se recomienda complementar la diferencia técnica con validación administrativa y contexto temporal.

La evidencia debe almacenarse con cuidado. Las salidas pueden revelar nombres de hosts, rangos internos, usuarios y versiones de software; su divulgación indiscriminada aumenta el riesgo. Un informe académico puede anonimizar identificadores y presentar ejemplos de interpretación sin publicar datos operativos sensibles. También conviene distinguir evidencia primaria —salida de herramienta— de análisis del estudiante —explicación y recomendaciones— para que el lector pueda evaluar la solidez de cada conclusión.

### **Formatos de evidencia**

- **`-oN output.txt`** — Salida legible en texto.
- **`-oX output.xml`** — Salida estructurada XML.

---

## 15. Reconocimiento Web Y Archivos Públicos

El historial contiene la descarga de robots.txt mediante wget y la lectura posterior del archivo. robots.txt es un recurso usado para expresar preferencias de rastreo a agentes automatizados; no constituye un mecanismo de control de acceso ni demuestra que los directorios mencionados estén disponibles. Su revisión puede ayudar a entender la estructura pública de un sitio, pero no autoriza el acceso a rutas protegidas. OWASP considera la revisión de metarchivos y la identificación de tecnologías parte de la recopilación de información en evaluaciones web. [4]

El reconocimiento web también puede considerar encabezados HTTP, certificados TLS, subdominios y tecnologías visibles, siempre dentro de los límites establecidos. Un nombre de servidor anunciado no siempre refleja la implementación real; una página de error puede pertenecer a un proxy, y un certificado puede incluir nombres que ya no están activos. La triangulación entre DNS, respuestas HTTP y registros públicos reduce errores de atribución. Además, las aplicaciones pueden depender de servicios externos, de modo que descubrir una relación técnica no equivale a demostrar propiedad sobre toda la infraestructura asociada.

En el material aparecen comprobaciones de conectividad mediante telnet hacia puertos específicos. En este contexto, telnet sirve como cliente TCP sencillo para comprobar si es posible establecer una conexión, no como prueba completa de seguridad del protocolo observado. Una conexión aceptada no identifica necesariamente el software ni sus permisos. El analista debe evitar interpretar un único mensaje de conexión como evidencia suficiente de exposición peligrosa.

---

## 16. Recon-Ng: Organización Del Reconocimiento Osint

El segundo archivo describe un flujo concreto en Recon-ng: iniciar el framework, listar espacios de trabajo, crear y cargar el espacio «Empresa», buscar módulos en el marketplace, instalar uno, cargarlo, consultar su información, establecer SOURCE y ejecutar run. Los espacios de trabajo permiten separar investigaciones y mantener sus datos organizados. Esta estructura es importante cuando una evaluación involucra varios dominios o cuando se necesita conservar trazabilidad entre fuentes y hallazgos. [5]

Recon-ng es un framework modular para recopilación de inteligencia de fuentes abiertas. En el archivo se citan módulos vinculados con resolución de nombres, registros WHOIS, transparencia de certificados, motores de búsqueda, servicios de información sobre dominios y relación entre bloques de red y organizaciones. La variedad de fuentes no garantiza exactitud uniforme. Algunos módulos dependen de servicios externos, claves de API, cuotas, cambios de interfaz o disponibilidad del proveedor; por ello, una instalación exitosa no equivale a obtener datos correctos.

El módulo recon/domains-hosts/hackertarget figura en la secuencia principal y se configura con SOURCE. Conceptualmente, se parte de un dominio autorizado para obtener nombres de hosts potencialmente relacionados. Los resultados deberían registrarse como candidatos hasta verificar su vigencia y atribución. Otros módulos del archivo, como certificate_transparency, ssl_san, whois_pocs, whois_orgs, netcraft, brute_hosts, google_site_web y bing_domain_web, representan fuentes o métodos diferentes de identificación. Algunos nombres incluyen «brute» pero pueden referirse a enumeración de nombres y no necesariamente a contraseñas; aun así, deben revisarse sus operaciones reales.

La lista del TXT incluye asimismo módulos bajo categorías discovery y exploitation, como command_injector y xpath_bruter. Estos últimos no pertenecen al reconocimiento pasivo ordinario y su presencia en una lista de instalación no demuestra que hayan sido ejecutados. Es indispensable diferenciarlos del objetivo académico de inventariar activos. En una metodología controlada se registran por separado las acciones de OSINT, la verificación activa y las pruebas intrusivas, reservando estas últimas para actividades expresamente autorizadas.

La principal contribución de Recon-ng es la organización de información dispersa. Su base de datos de trabajo permite relacionar dominios, hosts y otras entidades para construir hipótesis de infraestructura. El riesgo metodológico consiste en aceptar como cierto todo lo recuperado: los datos públicos pueden estar duplicados, caducos o referirse a empresas con nombres similares. La calidad del resultado depende de contrastar fuentes, fechar registros y documentar el criterio de atribución.

### **Flujo de trabajo de Recon-ng en los apuntes**

- **`workspaces create Empresa`** — Crear un espacio de trabajo.
- **`marketplace search`** — Explorar módulos.
- **`modules load recon/domains-hosts/hackertarget`** — Cargar módulo de reconocimiento.
- **`options set SOURCE www.sitio.com`** — Establecer la fuente autorizada.
- **`run`** — Ejecutar el módulo configurado.

---

## 17. Argus: Entorno Modular Y Límites De La Evidencia

El archivo Argus.txt registra la creación de un entorno virtual de Python, la clonación de un repositorio, la instalación de dependencias y una modificación local del código relacionada con argparse y cmd2. Estas operaciones preparan el entorno de ejecución; no constituyen por sí mismas escaneos de infraestructura. Posteriormente se documenta el inicio mediante python3 -m argus, la selección de un objetivo con set target dominio.com, la consulta de modules y varias instrucciones run identificadas por números. El material permite afirmar que se planeó una exploración modular, pero no identifica qué función correspondía a cada número en esa versión ni muestra resultados de las ejecuciones.

En particular, la lista run 1, run 2, run 3, run 4, run 5, run 8, run 9 80, run 9 100, run 10, run 12, run 18, run 19, run 32, run 54, run 100 y run 124 no debe convertirse en un catálogo inventado de técnicas. Los números pueden depender de la versión, del menú de módulos o de cambios en el proyecto. Para describirlos con precisión harían falta la salida de modules, la documentación correspondiente y los registros de cada ejecución. Esta cautela protege la calidad académica del informe.

Como concepto general, una herramienta modular reúne varias tareas bajo una interfaz común y permite seleccionar operaciones en función del objetivo. Sus ventajas potenciales son la comodidad, la repetición de procesos y la centralización de resultados. Sus riesgos incluyen ejecutar módulos sin conocer su impacto, confiar en dependencias desactualizadas o modificar el código sin pruebas suficientes. La intervención sobre el código observada en el archivo debe considerarse un ajuste local de compatibilidad, no una funcionalidad propia del escaneo.

La lección de esta sección es metodológica: conocer el nombre de una herramienta no sustituye la evidencia de su funcionamiento. Para futuras prácticas conviene guardar versión del repositorio, menú de módulos, parámetros de ejecución y salidas. Solo entonces es posible relacionar cada acción con una categoría de reconocimiento, escaneo, enumeración o prueba de seguridad.

### **Acciones registradas para Argus**

- **`python3 -m argus`** — Abrir la aplicación.
- **`set target dominio.com`** — Definir un objetivo.
- **`modules`** — Consultar los módulos.
- **`run <número>`** — Invocar un módulo por identificador; su función exacta no consta en el material.

---

## 18. Nessus Como Herramienta Complementaria

Nessus, desarrollado por Tenable, se utiliza para evaluar vulnerabilidades y configuraciones mediante conjuntos de comprobaciones. En esta práctica se menciona únicamente como herramienta relacionada, porque la actividad correspondiente todavía no se ha habilitado y no se aportaron resultados de su uso. Su función conceptual se ubica después de obtener un inventario de activos y servicios: permite investigar si determinadas versiones o configuraciones presentan problemas conocidos o incumplimientos de política.

La diferencia entre Nmap y Nessus no debe presentarse como una separación absoluta. Nmap puede ejecutar scripts de evaluación, y Nessus también necesita descubrir y caracterizar servicios. No obstante, sus enfoques principales son distintos: Nmap se utiliza ampliamente para cartografía de red y enumeración; Nessus organiza comprobaciones de vulnerabilidad y resultados orientados a remediación. Ambos requieren configuración adecuada, alcance autorizado y validación de hallazgos.

Un escáner de vulnerabilidades puede producir falsos positivos y falsos negativos. La detección basada en versiones puede ser engañosa cuando existen parches retroportados; las comprobaciones autenticadas pueden ofrecer más contexto que las no autenticadas, pero exigen proteger credenciales y controlar permisos. Las prioridades deben considerar gravedad técnica, exposición, criticidad del activo y posibilidad real de explotación. En ausencia de resultados de Nessus no es correcto afirmar que la práctica identificó vulnerabilidades específicas mediante esa herramienta.

---

## 19. Interpretación, Validación Y Priorización De Hallazgos

La fase de análisis transforma respuestas técnicas en información útil. Un hallazgo debe expresar qué se observó, cómo se observó, sobre qué activo, con qué limitaciones y por qué podría importar. Por ejemplo, «se detectó un servicio TCP accesible desde el segmento de laboratorio» es una observación; «el servicio permite acceso no autorizado» sería una conclusión adicional que necesita evidencia independiente. La calidad del informe depende de mantener separadas ambas afirmaciones.

Las observaciones pueden clasificarse por certeza: confirmadas mediante múltiples evidencias, probables por coincidencia de indicadores o pendientes de validación. También conviene distinguir riesgo y vulnerabilidad. El riesgo combina escenarios de amenaza, impacto y exposición; una vulnerabilidad es una debilidad concreta que puede contribuir a ese riesgo. Un servicio público legítimo puede representar superficie de ataque sin estar necesariamente mal configurado.

La priorización debe partir del contexto del activo. No es lo mismo un servicio administrativo expuesto a Internet que uno limitado a una red aislada de prácticas. Factores como sensibilidad de los datos, dependencia operativa, existencia de controles compensatorios y facilidad de corrección cambian la urgencia. El objetivo del escaneo no es producir la mayor cantidad de alertas, sino generar decisiones de seguridad justificadas y verificables.

Finalmente, la validación puede requerir conversación con administradores, consulta de configuraciones, comprobaciones de parches y repetición controlada de pruebas. Los resultados automáticos son un punto de partida. Un buen proceso documenta también aquello que no pudo confirmarse, pues la incertidumbre reconocida es preferible a una falsa sensación de precisión.

---

## 20. Aplicaciones Defensivas Del Escaneo De Infraestructura

El inventario de activos es una de las aplicaciones más directas. Los equipos no registrados, las interfaces adicionales y los servicios olvidados suelen escapar a los procesos de mantenimiento. Los escaneos periódicos, combinados con fuentes administrativas, ayudan a identificar estas diferencias. También permiten revisar segmentación: si un puerto administrativo es visible desde una red donde no debería estarlo, existe una señal para examinar las reglas de acceso, aunque todavía no se haya demostrado una vulnerabilidad.

Otra aplicación es el control de cambios. Al comparar resultados antes y después de una actualización, el equipo puede verificar si desapareció un servicio, cambió una versión o se modificó la exposición. Sin embargo, las comparaciones requieren condiciones semejantes: origen, horario, parámetros y disponibilidad de red. De lo contrario, una diferencia aparente podría reflejar una medición inconsistente. Guardar XML y salidas legibles facilita esta tarea.

En la gestión de incidentes, el reconocimiento puede ayudar a identificar qué servicios siguen accesibles y qué segmentos requieren revisión. Debe coordinarse con el equipo responsable para no interferir con la respuesta. En auditorías, aporta evidencia sobre la superficie de exposición observada y sobre el cumplimiento de políticas técnicas. En docencia, desarrolla competencias para formular hipótesis, diseñar pruebas y comunicar resultados sin confundir herramientas con conclusiones.

También puede servir para evaluar nuevas implementaciones antes de su puesta en producción. Una revisión controlada de puertos, servicios, DNS y certificados permite detectar exposiciones involuntarias. El valor preventivo aumenta cuando el proceso se integra en ciclos de mantenimiento y cuando las observaciones se traducen en acciones concretas: cerrar servicios innecesarios, reforzar autenticación, limitar accesos y mantener versiones soportadas.

---

## 21. Limitaciones, Falsos Resultados Y Consideraciones Éticas

Ningún escaneo ofrece visibilidad absoluta. Firewalls, sistemas de prevención, balanceadores, proxies, dispositivos apagados, servicios intermitentes y errores de resolución alteran lo observable. Un resultado depende del punto de origen: dos estaciones situadas en segmentos distintos pueden obtener mapas diferentes de la misma infraestructura. También influyen los privilegios de ejecución, las versiones de las herramientas y la carga del sistema. Por eso los resultados siempre deben presentarse como observaciones bajo condiciones específicas.

Los falsos positivos surgen cuando una señal se interpreta como evidencia de una condición inexistente; los falsos negativos aparecen cuando una condición real no se detecta. Ambos problemas afectan el valor de una evaluación. Las herramientas automatizadas aceleran el trabajo, pero no reemplazan la interpretación de protocolos ni la validación humana. El conocimiento técnico debe acompañarse de una actitud crítica frente a mensajes, banners, clasificaciones y datos procedentes de terceros.

La ética profesional exige minimizar el impacto y proteger los datos obtenidos. Las pruebas deben limitarse a sistemas autorizados y a los métodos acordados; los archivos de salida no deben publicarse sin revisión; las credenciales, si se utilizan en evaluaciones posteriores, deben gestionarse mediante procedimientos seguros. Un hallazgo sensible se comunica a los responsables y no se transforma en una demostración pública. Esta disciplina es parte de la competencia técnica, no una formalidad añadida.

---

## 22. Propuesta De Secuencia Didáctica Para La Práctica

Una secuencia razonable para un laboratorio comienza identificando las interfaces locales con ip a, verificando la subred autorizada y anotando la topología esperada. A continuación se realiza descubrimiento de hosts con -sn y se contrasta el resultado con las máquinas que deberían estar encendidas. Después se exploran puertos de uno o varios equipos seleccionados, usando un rango explícito para mantener control sobre la cobertura. Cada salida se guarda y se registra el contexto de ejecución.

La siguiente fase consiste en identificar servicios con -sV y, cuando sea pertinente, estimar el sistema operativo con -O. Si aparece SMB, se revisan scripts de enumeración previamente autorizados; si se detecta un servicio UDP de interés, se interpreta su estado considerando las limitaciones del protocolo. En paralelo, Recon-ng puede organizar información pública sobre un dominio de prueba, siempre distinguiendo candidatos de activos verificados. Argus se incorporaría únicamente después de documentar qué módulos ejecuta cada opción numérica.

Al terminar, se construye una matriz con columnas de activo, técnica, observación, nivel de certeza, relevancia y acción recomendada. Se comparan los hallazgos con el inventario del laboratorio y se señalan dudas pendientes. Nessus puede mencionarse en la discusión como una futura herramienta para profundizar en evaluación de vulnerabilidades, sin atribuirle ejecuciones que no se han realizado. Esta secuencia reproduce el sentido de los TXT y lo convierte en un proceso de aprendizaje verificable.

---

## 23. Discusión Integradora: Qué Se Puede Y Qué No Se Puede Concluir

Las tres fuentes de la práctica representan perspectivas complementarias. Nmap aporta observaciones directas sobre presencia de hosts, puertos, servicios y algunos parámetros de configuración. Recon-ng permite reunir datos públicos y organizar relaciones entre dominios, hosts y otras entidades. Argus muestra un entorno modular preparado para seleccionar acciones, aunque los materiales no permiten identificar las funciones concretas de cada número ejecutado. Ninguna de estas herramientas, por sí sola, certifica la seguridad integral de una organización.

Una de las enseñanzas más importantes es que la amplitud de opciones no equivale a calidad del diagnóstico. Un barrido de muchos puertos puede ser menos útil que una exploración limitada pero bien documentada. Un gran conjunto de subdominios puede contener numerosas entradas obsoletas. Un listado de usuarios o recursos compartidos no demuestra acceso indebido. La relevancia surge al relacionar datos con objetivos, contexto, autorización y controles esperados.

El reconocimiento también revela la naturaleza cambiante de las redes. La exposición depende de configuraciones temporales, actualizaciones, cambios DNS y políticas de segmentación. Por eso los resultados deben fecharse y revisarse cuando el entorno cambie. La práctica adquiere mayor valor cuando se interpreta como un proceso continuo de observación, contraste y mejora, no como una colección de comandos aislados.

---

## 24. Conclusiones

El reconocimiento y el escaneo de infraestructura constituyen una base técnica para comprender la superficie de exposición de una red. Su utilidad principal no consiste en encontrar automáticamente una falla, sino en reunir datos verificables sobre equipos, rutas, puertos, servicios y configuraciones. Las técnicas estudiadas muestran que cada capa de red aporta señales diferentes y que la interpretación depende del protocolo, la topología y las restricciones del entorno. Una respuesta positiva puede confirmar accesibilidad bajo ciertas condiciones; una ausencia de respuesta, en cambio, exige prudencia antes de concluir que un sistema no existe.

La práctica con Nmap permite relacionar conceptos teóricos con opciones concretas: descubrimiento de hosts, sondas TCP y UDP, detección de versiones, estimación de sistemas operativos, enumeración SMB, scripts NSE y formatos de salida. Recon-ng amplía el panorama hacia la inteligencia de fuentes abiertas y enseña a organizar información que requiere verificación. Argus introduce el valor y los riesgos de las herramientas modulares, al tiempo que recuerda la importancia de documentar qué hace cada módulo. Nessus se reconoce como un complemento para futuras actividades de evaluación de vulnerabilidades, sin atribuirle resultados inexistentes.

Desde una perspectiva profesional, la principal competencia adquirida es la capacidad de diseñar una evaluación responsable. Esto implica delimitar objetivos, respetar autorizaciones, escoger técnicas proporcionales, registrar evidencia, reconocer incertidumbres y traducir hallazgos en recomendaciones. El uso competente de herramientas no se mide por la cantidad de comandos ejecutados, sino por la claridad con que se explica qué se hizo, qué se observó y qué conclusiones están justificadas. Así, el escaneo deja de ser una actividad mecánica y se convierte en un proceso de análisis que contribuye a la administración y protección de los sistemas.

Finalmente, el estudio confirma que la seguridad no puede inferirse de una sola exploración. Los activos y servicios cambian, los controles pueden comportarse de manera distinta según el origen de la prueba y los resultados automáticos requieren validación. Integrar inventarios, revisión de configuraciones, gestión de vulnerabilidades y documentación continua permite que el reconocimiento cumpla una función preventiva. Esta visión resulta especialmente valiosa en la formación académica, porque promueve una práctica ética, reproducible y orientada a mejorar la infraestructura en lugar de limitarse a producir listados técnicos.

25. REFERENCIAS BIBLIOGRÁFICAS (FORMATO APA 7, CON ENLACES)

Scarfone, K., Souppaya, M., Cody, A., & Orebaugh, A. (2008). Technical guide to information security testing and assessment (NIST Special Publication 800-115). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-115

Lyon, G. F. (2009). Nmap network scanning: The official Nmap project guide to network discovery and security scanning. Insecure.Com LLC. https://nmap.org/book/

Nmap Project. (s. f.). Nmap reference guide. https://nmap.org/book/man.html

OWASP Foundation. (s. f.). Web security testing guide (versión 4.2): Information gathering. https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/01-Information_Gathering/

Recon-ng Project. (s. f.). Recon-ng: Open source web reconnaissance framework. https://recon-ng.org/

Tenable. (s. f.). Tenable Nessus documentation. https://docs.tenable.com/Nessus.htm

OWASP Foundation. (s. f.). Web security testing guide: Project overview. https://owasp.org/projects/web-security-testing-guide/

FUENTES DE LA PRÁCTICA (MATERIALES PROPORCIONADOS)

[P1] Material de práctica sin autor indicado. (s. f.). reconocimiento_escaneo_infraestructura(1).txt [Archivo de texto proporcionado para la actividad].
[P2] Material de práctica sin autor indicado. (s. f.). recon-ng.txt [Archivo de texto proporcionado para la actividad].
[P3] Material de práctica sin autor indicado. (s. f.). Argus.txt [Archivo de texto proporcionado para la actividad].

NOTA SOBRE CITAS: Las referencias numeradas [1] a [7] corresponden a fuentes externas. Las descripciones de comandos y secuencias concretas se basan en [P1], [P2] y [P3]. No se presentan resultados de escaneos no incluidos en esos materiales.

---
