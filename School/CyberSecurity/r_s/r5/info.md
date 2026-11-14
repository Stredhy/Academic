# Evasión de Defensas en Ciberseguridad

## 1. Definición y contexto

La **evasión de defensas** es el conjunto de técnicas que un adversario emplea para evitar la detección durante todas las fases de una intrusión: desde el acceso inicial hasta el impacto final. El objetivo es operar de forma invisible, haciendo que las herramientas de seguridad (AV, EDR, SIEM, firewalls) no identifiquen la actividad maliciosa.

Es la táctica más extensa del marco **MITRE ATT&CK** y, hasta 2026, la más utilizada por los atacantes en el mundo real.

---

## 2. Cambio estructural: ATT&CK v19 (abril 2026)

En **ATT&CK v19**, publicado el 28 de abril de 2026, MITRE retiró la táctica *Defense Evasion* (TA0005) y la dividió en dos nuevas tácticas basadas en la **intención del adversario**:

| Nueva táctica | ID | Intención | Ejemplos de técnicas |
|---|---|---|---|
| **Stealth** | TA0005 (hereda el ID) | Camuflarse dentro de comportamiento legítimo | Ofuscación, masquerading, LOLBins, inyección de proceso |
| **Defense Impairment** | TA0112 (nuevo) | Desactivar o degradar activamente los controles | Deshabilitar EDR, modificar firewall, borrar logs |

> **Nota:** En ATT&CK v20 (octubre 2026) este esquema se mantiene. La técnica T1562 (*Impair Defenses*) fue retirada y sus sub-técnicas reasignadas a la nueva táctica TA0112.

---

## 3. Técnicas principales

### 3.1 Ofuscación y codificación (T1027)

Transformar el payload para evitar la detección basada en firmas o análisis estático.

| Sub-técnica | ID | Método |
|---|---|---|
| Binary Padding | T1027.001 | Añadir bytes para alterar el hash |
| Software Packing | T1027.002 | UPX, Themida, VMProtect |
| Steganografía | T1027.003 | Ocultar payload en imágenes o audio |
| Compile After Delivery | T1027.004 | Entregar código fuente y compilar en la víctima |
| HTML Smuggling | T1027.006 | Construir payload en JavaScript del navegador |
| Dynamic API Resolution | T1027.007 | Resolver APIs en runtime, no en la import table |

### 3.2 Masquerading (T1036)

Disfrazar procesos, archivos o servicios maliciosos como componentes legítimos del sistema:
- Nominar un malware como `svchost.exe` y ejecutarlo desde `C:\Temp\`
- Usar nombres de procesos conocidos (`explorer.exe`, `winlogon.exe`)
- Colocar archivos en rutas legítimas (`%ProgramFiles%`, `System32`)

### 3.3 Living Off the Land (LOTL) y LOLBins (T1218)

**LOTL** consiste en abusar de herramientas nativas del sistema operativo en lugar de introducir software malicioso nuevo. Los **LOLBins** (Living Off the Land Binaries) son binarios firmados y de confianza que el atacante reutiliza:

| LOLBin | ID | Uso malicioso |
|---|---|---|
| `certutil.exe` | T1218.* | Descargar archivos, decodificar Base64 |
| `mshta.exe` | T1218.005 | Ejecutar HTA con VBScript/JScript |
| `regsvr32.exe` | T1218.010 | Cargar DLL remota (técnica *Squiblydoo*) |
| `rundll32.exe` | T1218.011 | Ejecutar funciones de DLL arbitraria |
| `msiexec.exe` | T1218.007 | Instalar MSI remoto con payload |
| `cmstp.exe` | T1218.003 | Ejecutar INF con comandos |
| `wmic.exe` | T1218.* | Ejecución vía XSL stylesheets |
| `InstallUtil.exe` | T1218.004 | Ejecutar .NET assembly |

El proyecto **LOLBAS** documenta más de 200 binarios, scripts y librerías Windows explotables.

> **Detección:** Los EDRs modernos detectan bien cadenas clásicas (`certutil -urlcache`, `regsvr32 /s /u /i:http://...`), pero cadenas más nuevas (`curl.exe` + `tar.exe` en Windows 10+) aún tienen baselines inmaduras.

### 3.4 Inyección de proceso (T1055)

Ejecutar código malicioso dentro del espacio de memoria de un proceso legítimo para evadir defensas basadas en proceso:

- **DLL Injection** (T1055.001): Inyectar una DLL en un proceso en vivo
- **PE Injection** (T1055.002): Inyectar un ejecutable portable
- **Thread Execution Hijacking** (T1055.003): Secuestrar hilos existentes
- **APC Injection** (T1055.004): Inyectar código mediante la cola de llamadas asíncronas
- **Process Hollowing**: Crear un proceso legítimo en estado suspendido, vaciar su memoria y cargar el payload malicioso
- **Reflective DLL Loading** (T1620): Cargar una DLL completamente en memoria sin tocar disco

### 3.5 Eliminación de indicadores (T1070)

- **Clear Windows Event Logs** (T1070.001): Borrar registros de eventos (Event ID 1102)
- **File Deletion** (T1070.004): Eliminar herramientas o payloads del disco
- **Timestomping**: Modificar metadatos de tiempo (MFT) para que archivos maliciosos parezcan antiguos
- **Alternative Data Streams (ADS)**: Ocultar datos en streams alternativos del NTFS

### 3.6 Evasión de virtualización y sandbox (T1497)

- Detectar entornos virtualizados (VMware, VirtualBox, Hyper-V)
- Verificar tiempos de ejecución, número de CPUs, memoria disponible
- Ejecutar el payload solo en entornos "reales"

### 3.7 Execution Guardrails (T1480)

El malware solo se activa bajo condiciones específicas:
- **Time-based**: Ejecutar solo en horarios o fechas determinadas
- **Location-based**: Solo en ciertos países o redes
- **Domain-based**: Solo en dominios corporativos específicos

---

## 4. Evasión avanzada de EDR

Los EDR modernos monitorizan a múltiples niveles (user-mode hooks, ETW, kernel callbacks). La evasión se ha convertido en un juego de capas:

| Capa defensiva | Técnica de evasión | Detección residual |
|---|---|---|
| AV / Firmas | Ofuscación, packing | Análisis de comportamiento |
| AMSI | Patch de `amsi.dll`, bypass de `AmsiScanBuffer` | ETW Threat Intelligence |
| EDR user-mode hooks | API Unhooking, Direct/Indirect Syscalls (SysWhispers2) | Secuencias anómalas de syscalls, backtraces |
| ETW (Event Tracing) | ETW Patching, nulling de providers | Kernel callbacks |
| Kernel callbacks | BYOVD (Bring Your Own Vulnerable Driver) | Driver load monitoring, HVCI |
| Memory forensics | Ofuscación de memoria, sleep obfuscation | Muy difícil de evadir completamente |

### BYOVD (Bring Your Own Vulnerable Driver)

Técnica de alto impacto: el atacante carga un **controlador del kernel firmado pero vulnerable** (no incluido en la blocklist de Microsoft) para obtener acceso a nivel de kernel y desde ahí:
- Matar procesos del EDR
- Desregistrar callbacks del kernel
- Obtener privilegios irreversibles

**Defensa:** Habilitar **HVCI** (Hypervisor-protected Code Integrity) y la **Vulnerable Driver Blocklist** de Microsoft.

### HookChain (DEF CON 32)

Técnica que aprovecha la capa del subsistema situada por encima de `ntdll.dll`, donde el **94% de las soluciones EDR** carecen de puntos de control. Logró una tasa de éxito del 88% en la elusión de 26 soluciones EDR analizadas.

### Evolución temporal de las técnicas de evasión de EDR

| Período | Tendencias |
|---|---|
| 2018–2019 | AMSI bypass básico, patcheo de `amsi.dll` |
| 2020–2021 | Ofuscación de memoria, sleep obfuscation (Ekko, Zilean) |
| 2021–2023 | SysWhispers2, indirect syscalls, ThreadStackSpoofer, FreshyCalls |
| 2024–2026 | HookChain, BYOVD masivo, evasión multi-agente autónoma, ofuscación de suspensión avanzada |

---

## 5. Evasión en entornos cloud

| Técnica | ID | Descripción |
|---|---|---|
| Deploy Container | T1610 | Desplegar contenedores para ejecutar payload o evadir defensas |
| Temporary Elevated Cloud Access | — | Abusar de configuraciones que otorgan acceso elevado temporal a recursos cloud |
| Modify Cloud Compute Infrastructure | — | Modificar arquitectura de cómputo cloud para ocultar actividad |
| Execution Guardrails (cloud) | T1480 | Ejecutar solo en regiones o instancias específicas |

---

## 6. Estrategias de detección y defensa

### Princip


### Recomendaciones clave

1. **Correlación de eventos**: Ningún indicador aislado es suficiente; buscar cadenas de comportamiento (padre-hijo, secuencias de syscalls, patrones de red).
2. **Script Block Logging + AMSI**: Configurar en todos los endpoints; es la principal defensa contra PowerShell ofuscado.
3. **HVCI + Vulnerable Driver Blocklist**: Mitiga BYOVD de forma efectiva.
4. **Application Allowlisting / App Control for Business**: Limitar qué binarios pueden ejecutarse en servidores y estaciones de administración.
5. **Sigma rules y KQL/Sentinel**: Detección de cadenas LOLBin anómalas (p. ej., `certutil -urlcache` + `mshta` + `PowerShell`).
6. **Tamper Protection**: Proteger los agentes EDR contra deshabilitación local.
7. **Log forwarding centralizado**: Evitar que el borrado local de logs (Event 1102) elimine la evidencia.
8. **Baselining y detección de anomalías**: Establecer líneas base de comportamiento normal para detectar desviaciones.
9. **Red teaming regular**: Probar la efectividad de las defensas con técnicas reales de evasión.

---

## 7. Herramientas de referencia

| Herramienta / Proyecto | Propósito |
|---|---|
| [LOLBAS](https://lolbas-project.github.io) | Catálogo de binarios/scripts/librerías Windows explotables |
| [SysWhispers2](https://github.com/jthuraisamy/SysWhispers2) | Generador de indirect syscalls |
| [Invoke-Obfuscation](https://github.com/cobbr/Invoke-Obfuscation) | Ofuscación de scripts PowerShell |
| [Sigma](https://github.com/SigmaHQ/sigma) | Reglas de detección agnósticas a la plataforma |
| [MITRE ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) | Visualización y mapeo de técnicas |
| [ThreatCheck / DefenderCheck](https://github.com/Neo23x0) | Análisis de detección por AV/Defender |

---

## 8. Conclusión

La evasión de defensas es un **juego de gato y ratón en constante evolución**. El cambio a ATT&CK v19/v20 refleja la madurez del marco: separar *camuflarse* (Stealth) de *destruir controles* (Defense Impairment) permite a los defensores priorizar mejor sus inversiones. La detección efectiva ya no depende de una sola capa, sino de la **correlación entre capas**, el **análisis de comportamiento** y la **capacidad de respuesta rápida** ante las técnicas emergentes.   io: defensa en profundidad
   
- Capa 1: AV/Firmas → Evasión: ofuscación, packing
- Capa 2: AMSI → Evasión: AMSI bypass
- Capa 3: EDR user-mode → Evasión: unhooking, direct syscalls
- Capa 4: ETW kernel → Evasión: ETW patching
- Capa 5: Kernel callbacks → Evasión: BYOVD
- Capa 6: Memory forensics → Evasión: muy difícil de evadir completamente

Cada bypass deja artefactos detectables por otra capa.


### Recomendaciones clave

1. **Correlación de eventos**: Ningún indicador aislado es suficiente; buscar cadenas de comportamiento (padre-hijo, secuencias de syscalls, patrones de red).
2. **Script Block Logging + AMSI**: Configurar en todos los endpoints; es la principal defensa contra PowerShell ofuscado.
3. **HVCI + Vulnerable Driver Blocklist**: Mitiga BYOVD de forma efectiva.
4. **Application Allowlisting / App Control for Business**: Limitar qué binarios pueden ejecutarse en servidores y estaciones de administración.
5. **Sigma rules y KQL/Sentinel**: Detección de cadenas LOLBin anómalas (p. ej., `certutil -urlcache` + `mshta` + `PowerShell`).
6. **Tamper Protection**: Proteger los agentes EDR contra deshabilitación local.
7. **Log forwarding centralizado**: Evitar que el borrado local de logs (Event 1102) elimine la evidencia.
8. **Baselining y detección de anomalías**: Establecer líneas base de comportamiento normal para detectar desviaciones.
9. **Red teaming regular**: Probar la efectividad de las defensas con técnicas reales de evasión.

---

## 7. Herramientas de referencia

| Herramienta / Proyecto | Propósito |
|---|---|
| [LOLBAS](https://lolbas-project.github.io) | Catálogo de binarios/scripts/librerías Windows explotables |
| [SysWhispers2](https://github.com/jthuraisamy/SysWhispers2) | Generador de indirect syscalls |
| [Invoke-Obfuscation](https://github.com/cobbr/Invoke-Obfuscation) | Ofuscación de scripts PowerShell |
| [Sigma](https://github.com/SigmaHQ/sigma) | Reglas de detección agnósticas a la plataforma |
| [MITRE ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) | Visualización y mapeo de técnicas |
| [ThreatCheck / DefenderCheck](https://github.com/Neo23x0) | Análisis de detección por AV/Defender |

---

## 8. Conclusión

La evasión de defensas es un **juego de gato y ratón en constante evolución**. El cambio a ATT&CK v19/v20 refleja la madurez del marco: separar *camuflarse* (Stealth) de *destruir controles* (Defense Impairment) permite a los defensores priorizar mejor sus inversiones. La detección efectiva ya no depende de una sola capa, sino de la **correlación entre capas**, el **análisis de comportamiento** y la **capacidad de respuesta rápida** ante las técnicas emergentes.   


# Seguridad en la Nube (Cloud Security)

## 1. Definición y contexto

La **seguridad en la nube** es el conjunto de prácticas, controles, tecnologías y marcos de gobernanza diseñados para proteger datos, aplicaciones y recursos de infraestructura desplegados en entornos cloud (IaaS, PaaS, SaaS, serverless). Su objetivo es garantizar la **confidencialidad, integridad y disponibilidad** de los activos digitales, asumiendo que el perímetro tradicional ya no existe.

En 2026, la seguridad cloud se ha consolidado como la disciplina central de la ciberseguridad empresarial. Los datos son contundentes:

| Métrica | Valor | Fuente |
|---|---|---|
| Costo promedio global de un breach | **$4.99M** (récord histórico, +12% YoY) | IBM 2026 |
| Costo en la nube pública | **$5.38M** | IBM 2026 |
| Breaches multi-entorno | 30% (costo promedio $5.39M) | IBM 2026 |
| Tiempo medio de identificación y contención | **247 días** | IBM 2026 |
| Breaches con ransomware | 48% | Verizon 2026 DBIR |
| Breaches con elemento humano | 62% | Verizon 2026 DBIR |
| Breaches con participación de terceros | 48% (vs. 30% en 2025) | Verizon 2026 DBIR |
| Ataques sin malware (credenciales válidas) | 79% | CrowdStrike |
| Breaches habilitados por IA | 1 de cada 4 (+56% YoY) | IBM 2026 |

> **Dato clave:** El 99% de los fallos de seguridad en la nube son responsabilidad del **cliente**, no del proveedor (Gartner).  El modelo de responsabilidad compartida significa que el proveedor protege *la* nube, pero el cliente protege *en* la nube.

---

## 2. Modelo de Responsabilidad Compartida

El pilar conceptual de toda la seguridad cloud. Cada servicio tiene un reparto distinto:

| Modelo | Proveedor (CSP) | Cliente |
|---|---|---|
| **IaaS** (EC2, VMs) | Hardware, hipervisor, red física, datacenter | SO, parches, IAM, datos, aplicaciones, firewalls de red |
| **PaaS** (App Engine, Functions) | SO, runtime, red, hardware | Datos, aplicaciones, IAM, configuración de red |
| **SaaS** (Office 365, Salesforce) | Todo: infraestructura, plataforma, aplicación | Datos, cuentas, configuración de acceso, políticas de retención |
| **Serverless** (Lambda, Cloud Functions) | Infraestructura, runtime, escalado | Código, datos, IAM, configuración de triggers |

> **Práctica:** Documentar el modelo de responsabilidad compartida **por cada servicio en uso**.  Los equipos que no lo hacen asumen implícitamente que el proveedor cubre todo.

---

## 3. Principales amenazas y vectores de ataque

### 3.1 Clasificación por impacto

| Vector de ataque | % de breaches | Ejemplo |
|---|---|---|
| **Abuso de credenciales / secretos robados** | 22% | Claves API en repositorios, service accounts sin rotar |
| **Malconfiguración** | 60% de breaches de datos cloud | S3 público, RDS expuesto a 0.0.0.0/0 |
| **Supply chain / pipeline** | Crecimiento más rápido | Dependencias comprometidas, imágenes Docker maliciosas |
| **Ataques a IA / agentes** | Emergente, sin baseline | Prompt injection, data poisoning, abuso de agentes |
| **Explotación de vulnerabilidades** | 31% (vector #1 en 2026) | CVEs en workloads cloud, RCE en contenedores |

### 3.2 Técnicas cloud específicas (MITRE ATT&CK)

El marco **MITRE ATT&CK** no tiene una "matriz cloud" separada: es la matriz Enterprise filtrada a plataformas cloud (IaaS, SaaS, Identity Provider, Office Suite).  En **ATT&CK v20** (octubre 2026) la matriz Enterprise contiene 227 técnicas y 479 sub-técnicas. 

Las técnicas cloud más explotadas:

| Técnica | ID | Descripción |
|---|---|---|
| Valid Accounts: Cloud Accounts | T1078.004 | Login con credenciales robadas, sin malware |
| Additional Cloud Credentials | T1098.001 | Plantar credenciales para persistencia |
| Cloud Instance Metadata API | T1552.005 | Robar credenciales temporales de la workload |
| Disable or Modify Cloud Logs | T1562.008 | Cegar la detección |
| Data from Cloud Storage | T1530 | Exfiltración de buckets / blobs |
| Cloud API | T1059.009 | Ejecución vía API cloud (IAM, Compute, Storage) |
| Serverless Execution | T1610 | Abuso de funciones serverless como vector |
| Forge Web Credentials: SAML Tokens | T1550.005 | Forjamiento de tokens SAML para SaaS |
| Anti-Automation Evasion | T1497.005 | Evadir CAPTCHA / rate limiting en APIs cloud |

> **Nota ATT&CK v19/v20:** La táctica *Defense Evasion* (TA0005) fue reemplazada por **Stealth** y **Defense Impairment** (TA0112), aplicable también a entornos cloud.

### 3.3 Amenazas emergentes: IA en la nube

| Tipo de breach de IA | % de breaches de IA | Costo promedio |
|---|---|---|
| Malconfiguración de seguridad cloud | 27% | $5.25M |
| Compromiso de apps/APIs/plug-ins conectados | 27% | $4.37M |
| Data poisoning | 26% | $4.32M |
| Model inversion | 25% | $6.07M |
| Prompt injection | 25% | $5.89M |

- **21%** de las organizaciones comprometidas reportaron un incidente relacionado con un modelo o aplicación de IA (vs. 13% en 2025). 
- **92%** de esas organizaciones **no tenían controles de acceso adecuados** sobre sus modelos de IA. 

---

## 4. Arquitectura de seguridad cloud

### 4.1 Zero Trust en la nube

En 2026, **Zero Trust** dejó de ser una aspiración y se convirtió en la postura por defecto.  Gartner estima que al final de 2026, el 10% de las grandes empresas tendrá un programa Zero Trust maduro (vs. <1% en 2023). 

**Principios fundamentales (NIST SP 800-207):**

| Principio | Aplicación cloud |
|---|---|
| Never trust, always verify | Cada request es autenticada y autorizada, sin importar si viene de dentro o fuera de la VPC |
| Least privilege | IAM roles con permisos mínimos, JIT access, expiración automática |
| Assume breach | Microsegmentación, mTLS entre servicios, aislamiento de workloads |
| Continuous monitoring | Detección de anomalías en tiempo real, scoring de riesgo dinámico |

**Pillares de implementación:**

| Pilar | Tecnologías clave |
|---|---|
| Identity | MFA FIDO2/passkeys, SSO, PAM, workload identity (SPIFFE/SPIRE) |
| Network | ZTNA, microsegmentación, service mesh (Istio/Envoy), mTLS |
| Workload | App Control, allowlisting, runtime protection |
| Data | Clasificación, tokenización, ABAC, DLP |
| Device/Endpoint | Posture checks, EDR, device compliance |

> **Dato de adopción:** 82% de las organizaciones consideran ZTNA esencial, pero solo **17%** lo han implementado completamente.  La brecha de ejecución es de 65 puntos.

### 4.2 Segmentación de red

| Dimensión | Segmentación por IP | Microsegmentación por identidad |
|---|---|---|
| Ancla de confianza | Ubicación de red | Identidad de workload (SPIFFE, IAM Role) |
| Estabilidad de política | Se rompe con cambios de IP | Sobrevive a escalado, migración, redeploy |
| Superficie de ataque | Tráfico east-west amplio | Default-deny; política explícita |
| Respuesta a incidentes | Aislamiento manual de VLAN | Cuarentena dinámica de workload por política |
| Soporte multi-cloud | Fragmentado | Consistente entre AWS, Azure, GCP |

---

## 5. Identidad y acceso (IAM)

La **identidad es la superficie de ataque #1** en la nube, por encima de la red. 

### 5.1 Controles esenciales

| Control | Detalle |
|---|---|
| **MFA obligatorio** | FIDO2/WebAuthn para cuentas privilegiadas. SMS no cumple NIST SP 800-63B high-assurance |
| **Least privilege** | Auditar roles cada 90 días; eliminar permisos no usados |
| **JIT Access** | Acceso privilegiado temporal con expiración automática |
| **Workload Identity Federation** | Reemplazar API keys estáticas por credenciales federadas temporales (AWS IAM Roles Anywhere, Azure Managed Identities) |
| **PAM** | Vaulting de credenciales, grabación de sesiones, eliminación de standing admin |
| **Passwordless** | Passkeys y hardware keys; reducción del 99.9% en cuentas comprometidas (Microsoft) |
| **Root/Global Admin** | Nunca usar para operaciones diarias; MFA + vault + cuentas separadas con scope |

### 5.2 Machine identities

- Service accounts, API keys y workload credentials suelen **superar a los usuarios humanos por un orden de magnitud**. 
- Frecuentemente sobre-privilegiadas y con rotación deficiente.
- **Solución:** Workload identity federation + rotación automática + monitoreo de uso anómalo. 

---

## 6. Protección de datos

### 6.1 Cifrado

| Contexto | Estándar |
|---|---|
| At rest | AES-256 (KMS, HSM) |
| In transit | TLS 1.2 mínimo, TLS 1.3 recomendado; mTLS entre servicios internos |
| Claves | KMS o HSM dedicado; rotación programada; CMK para datos sensibles |
| Secrets | Secrets Manager (versionado, rotación, retrieval JIT) — NUNCA en código o repositorios |

### 6.2 Clasificación y gobernanza

- Clasificar datos por sensibilidad (público, interno, confidencial, restringido).
- Aplicar **ABAC** (Attribute-Based Access Control) en puntos de acceso a datos.
- **DLP** (Data Loss Prevention) para prevenir exfiltración.
- Backups inmutables y aislados (protección contra ransomware).

---

## 7. Seguridad de contenedores y Kubernetes

| Área | Control |
|---|---|
| Imágenes | Escaneo de vulnerabilidades en CI/CD antes del deploy (Trivy, Grype, Snyk) |
| Runtime | CWPP (Container Workload Protection): monitoreo de procesos, archivos, red |
| Orquestación | RBAC en Kubernetes, Network Policies, admission controllers (OPA/Gatekeeper) |
| Secrets | External Secrets Operator, Vault, o cloud-native secrets managers |
| Hardening | Non-root users, read-only filesystems, no privileged mode, resource limits |
| Supply chain | SBOM, cosign/sigstore para firma de imágenes, admission de imágenes firmadas |

---

## 8. Infraestructura como Código (IaC) y DevSecOps

### 8.1 Shift-left

| Fase | Control |
|---|---|
| Pre-commit | Detección de secrets en código (gitleaks, trufflehog) |
| CI/CD | Escaneo de IaC (Terraform, CloudFormation, Pulumi) — bloquear merge si crea exposición pública |
| Build | SCA (Software Composition Analysis), SAST, escaneo de imágenes |
| Deploy | Policy as Code (OPA, Sentinel, Conftest) |
| Runtime | CSPM continuo, CWPP, detección de amenazas |

### 8.2 Policy as Code

- Definir políticas de seguridad como código versionado y auditable.
- Ejemplos: OPA Rego, AWS SCPs, Azure Policy, GCP Org Policies.
- Permitir auto-remediación: cerrar la brecha entre detección y fix. 

---

## 9. Monitoreo, detección y respuesta

### 9.1 Logging y telemetría

| Fuente | Servicio |
|---|---|
| AWS | CloudTrail (multi-región + log file validation), VPC Flow Logs, GuardDuty |
| Azure | Activity Logs, Defender for Cloud, Sentinel |
| GCP | Cloud Logging, Security Command Center (SCC) |
| Universal | Forwarding a SIEM centralizado, alertas en tiempo real |

> **Crítico:** Habilitar logging en **todas las regiones** y hacer forwarding centralizado.  El borrado local de logs (T1562.008) no debe eliminar la evidencia.

### 9.2 Detección de amenazas

| Señal | Ejemplo |
|---|---|
| Impossible travel | Login desde dos países en <10 min |
| Privilege escalation | Role con `*:*` creado por un usuario no-admin |
| Bulk data download | S3 GetObject >10k en 1 hora |
| API anomalous | Llamadas a APIs IAM desde una workload que nunca las usó |
| Metadata API abuse | curl a 169.254.169.254 desde un contenedor |

### 9.3 Incident response

- Plan documentado y probado (tabletop exercises ≥2x/año).
- SLAs de remediación: **Crítico 24-72h, Alto 7-14 días, Medio 30 días**. 
- KPI: **MTTR** (Mean Time to Remediate). 

---

## 10. Herramientas y plataformas

### 10.1 CNAPP (Cloud-Native Application Protection Platform)

En 2026, el CSPM standalone se ha absorbido en plataformas CNAPP más amplias:

| Plataforma | Mejor para | Modelo de despliegue | Diferenciador |
|---|---|---|---|
| **Wiz** (adquirida por Google, $32B, marzo 2026) | Multi-cloud, análisis de ataque paths | Agentless | Security Graph, >45% Fortune 100 |
| **Palo Alto Prisma Cloud** | Enterprise multi-cloud, compliance | Agentless + Agent | 100+ frameworks de compliance |
| **Orca Security** | Agentless CNAPP | Agentless | SideScanning |
| **CrowdStrike Falcon Cloud** | Unificación EDR + cloud | Agent-first + Agentless | 281+ grupos adversarios |
| **Microsoft Defender for Cloud** | Ecosistema Azure | Agentless nativo | Tier gratuito, integración nativa |
| **FortiCNAPP (Lacework)** | Ecosistema Fortinet | Agentless + Agent | CDR conductual |

### 10.2 Categorías de herramientas

| Categoría | Función | Ejemplos |
|---|---|---|
| CSPM | Detección de malconfiguración y compliance | Wiz, Prisma, Defender for Cloud, Prowler |
| CWPP | Protección de workloads en runtime | Falcon Cloud, Lacework, Aqua |
| CWIS | Workload Identity & Secrets | HashiCorp Vault, AWS Secrets Manager |
| CASB | Visibilidad y control de SaaS | Zscaler, Palo Alto Prisma Access |
| SIEM/SOAR | Correlación y orquestación | Splunk, Sentinel, Datadog SIEM |
| IaC Security | Escaneo de plantillas | Checkov, tfsec, Terrascan |
| SCA | Dependencias vulnerables | Snyk, Dependabot, Trivy |
| DAST | Pruebas dinámicas de apps | OWASP ZAP, Burp Suite |

---

## 11. Compliance y marcos

| Marco | Alcance cloud |
|---|---|
| **NIST SP 800-53** | Controles de seguridad federales (US) |
| **CIS Benchmarks** | Configurations hardened por servicio cloud |
| **ISO 27001** | Gestión de seguridad de la información |
| **SOC 2** | Controles de seguridad, disponibilidad, confidencialidad |
| **PCI DSS** | Datos de tarjetas (entorno cloud incluido) |
| **GDPR / LGPD** | Protección de datos personales (EU / MX) |
| **CSA CCM v4.1** | 200+ controles en 17 dominios cloud; mapeado a ATT&CK (ene 2026) |
| **CIS Zero Trust Maturity Model** | Roadmap de madurez Zero Trust |

> **Tendencia 2026:** El US National Cybersecurity Strategy (marzo 2026) exige Zero Trust y criptografía post-cuántica como requisitos de compliance para contratistas federales. 

---

## 12. Seguridad en entornos multi-cloud e híbridos

| Reto | Estrategia |
|---|---|
| Inconsistencia de políticas | Policy as Code uniforme (OPA, Sentinel) |
| Fragmentación de visibilidad | CNAPP multi-cloud + SIEM centralizado |
| Identidad dispersa | IdP central (Entra ID, Okta) + workload federation |
| Red híbrida | SD-WAN + ZTNA + microsegmentación |
| Egress control | Private endpoints, VPC peering, no internet para workloads internas |

---

## 13. Checklist de implementación (priorizado)

| # | Acción | Impacto | Esfuerzo | Cuándo |
|---|---|---|---|---|
| 1 | MFA en todas las cuentas (especialmente root/global admin) | Muy alto | Bajo | **Hoy** |
| 2 | Eliminar acceso público de bases de datos y storage | Muy alto | Bajo | **Hoy** |
| 3 | Dejar de usar root/admin para operaciones diarias | Alto | Bajo | Esta semana |
| 4 | Habilitar audit logging en todas las regiones | Alto | Bajo | Esta semana |
| 5 | Enforcing least privilege / eliminar wildcards IAM | Alto | Medio | Ongoing |
| 6 | Cifrado at rest + in transit (TLS 1.2+) | Alto | Bajo | Ahora |
| 7 | Activar threat detection (GuardDuty / Defender / SCC) | Alto | Bajo | Esta semana |
| 8 | Backups inmutables y aislados | Alto | Medio | Antes del ransomware |
| 9 | Desplegar CSPM / compliance continuo | Medio-alto | Medio | Una vez los básicos |
| 10 | Guardrails organizacionales (SCPs / Azure Policy / Org Policies) | Alto | Alto | >2 cuentas |

---

## 14. Tendencias 2026–2027

| Tendencia | Detalle |
|---|---|
| **Zero Trust como baseline** | Ya no es "tendencia"; es el estándar mínimo.  Gartner: 10% de grandes empresas con programa maduro en 2026 |
| **IA en la defensa** | AI SOCs, detección autónoma, scoring de riesgo dinámico, respuesta automatizada |
| **IA como ataque** | 1 de cada 4 breaches maliciosos es AI-enabled (+56% YoY).  Prompt injection, deepfakes para phishing, agentes autónomos |
| **Post-cuántica** | Migración a criptografía resistente a quantum (PQC) exigida por regulación federal US |
| **Consolidación CNAPP** | CSPM standalone casi extinto; las plataformas unifican posture + runtime + identity + data |
| **Supply chain cloud** | SBOM obligatorio, firma de imágenes, verificación de paquetes en CI/CD |
| **Agentes de IA como identidades** | Cisco, CrowdStrike y otros extienden Zero Trust a agentes de IA (identidad, permisos, auditoría) |
| **Denial of Wallet** | Nuevo tipo de ataque: agotamiento de recursos cloud para generar facturas exorbitantes |

---

## 15. Conclusión

La seguridad en la nube en 2026 gira en torno a tres pilares:

1. **Identidad como perímetro** — El control de mayor apalancamiento no es un firewall ni un WAF; es el IAM. MFA, least privilege, workload identity federation y PAM resuelven la mayoría de los vectores de ataque reales.
2. **Zero Trust como arquitectura** — No es un proyecto; es una postura.  Cada request se verifica, el acceso es mínimo y temporal, y la asunción es que el entorno ya está comprometido.
3. **Automatización continua** — CSPM/CNAPP, policy as code, auto-remediación y detección basada en comportamiento reemplazan las revisiones manuales periódicas que no pueden seguir el ritmo de cambio cloud. 

El 99% de los incidentes son responsabilidad del cliente. La inversión que más reduce riesgo no es la más cara ni la más sofisticada: es **cerrar las malconfiguraciones, eliminar el acceso público innecesario, y garantizar que cada identidad (humana o máquina) tenga solo los permisos que necesita, solo cuando los necesita**.   