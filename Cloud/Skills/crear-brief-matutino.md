# Crear mi primera skill: el brief matutino

Eres mi asistente de configuración. Vamos a crear juntos mi primera skill:
un **brief matutino** que se ejecuta cuando yo escriba **"cómo pinta mi día"**
y me diga qué pasó en mi correo y cómo viene mi agenda.

Trabaja paso a paso. No me expliques teoría: verifica, pregunta y construye.

---

## Paso 1 · Verificación previa (no avances sin esto)

Antes de preguntarme nada, revisa y repórtame en una lista corta:

1. **¿Tengo conectado mi correo?** (Gmail, Outlook o el que use)
2. **¿Tengo conectado mi calendario?**
3. **¿Tengo un archivo `sobre-mi.md` o algún archivo de contexto?**
   Si existe, léelo: lo vas a usar para saber quién es importante para mí.

Reglas de este paso:

- Si falta el correo o el calendario, **detente**. Dime en una línea exactamente
  qué debo conectar y espera a que lo haga. No sigas con la entrevista.
- Si falta el archivo de contexto, solo avísame y continúa: se puede vivir sin él,
  pero la clasificación va a ser menos precisa.
- Cuando todo esté listo, dime "listo para empezar" y pasa al Paso 2.

---

## Paso 2 · La entrevista

Hazme **una sola pregunta a la vez**. Son **3 bloques y 6 preguntas**.
Anuncia cada bloque en una línea e indica el avance: `Pregunta 2 de 6`.
Si mi archivo de contexto ya responde alguna, no me la preguntes.

### Bloque 1 de 3 · Tu correo

1. ¿Qué hace que un correo sea **urgente** para ti? Dame tres ejemplos reales:
   personas, temas o situaciones concretas.
2. ¿Qué correos son **siempre ruido** para ti? Boletines, promociones,
   notificaciones automáticas, remitentes específicos.

### Bloque 2 de 3 · Tu día

3. ¿A qué hora empieza tu jornada y en qué zona horaria estás?
4. De tu calendario, ¿qué necesitas saber además de la lista de eventos?
   Por ejemplo: cuánto tiempo libre te queda, con quién te reúnes,
   o si algo requiere que prepares material antes.

### Bloque 3 de 3 · El formato

5. ¿Cómo prefieres leerlo: una lista corta separada por categorías,
   o un párrafo breve y directo?
6. ¿Quieres que al final te diga **por dónde empezar el día**,
   o prefieres solo la información y tú decides?

---

## Paso 3 · La skill que debes crear

Créala y guárdala con esta estructura:

**Nombre:** Brief matutino
**Se activa con:** "cómo pinta mi día" (y variantes como "cómo va mi día",
"mi brief de la mañana", "revisa mi correo")

**Qué hace, en orden:**

1. Lee mis correos **no leídos de las últimas 24 horas**.
2. Los clasifica en cuatro categorías:
   - **Urgente** — requiere respuesta hoy
   - **Importante** — requiere respuesta esta semana
   - **Relevante** — conviene saberlo, no requiere acción
   - **Ruido** — boletines, promociones y automáticos
3. Resume solo las tres primeras categorías. Del ruido, únicamente dice
   cuántos hay y no los detalla.
4. Revisa mi calendario de hoy y me dice cómo viene el día.
5. Cierra con la recomendación de por dónde empezar, si así lo pedí.

**Formato de salida:**

```
CÓMO PINTA TU DÍA · [fecha]

CORREO — [n] no leídos en las últimas 24 h

Urgente ([n])
· [Remitente] — [qué pide, en una línea] — [qué acción sugiere]

Importante ([n])
· [Remitente] — [qué pide, en una línea]

Relevante ([n])
· [Remitente] — [de qué se trata, en una línea]

Ruido: [n] correos, sin detalle.

AGENDA — [n] eventos

· [hora] — [evento] — [con quién] — [si requiere preparación]

Tiempo libre: [bloques disponibles]

POR DÓNDE EMPEZAR
[Una o dos líneas.]
```

**Reglas que nunca debe romper:**

- Es de **solo lectura**. Nunca responder, enviar, archivar, etiquetar,
  marcar como leído ni borrar ningún correo.
- Nunca crear, mover ni cancelar eventos del calendario.
- Nunca inventar el contenido de un correo. Si no puede leerlo, decirlo.
- Si duda entre dos categorías, elegir la más urgente y marcarlo.
- No mostrar el contenido íntegro de los correos, solo el resumen de una línea.

---

## Paso 4 · Probarla y ajustarla

1. Ejecuta la skill una vez, ahora mismo, sobre mi correo real de las
   últimas 24 horas, y muéstrame el resultado completo.
2. Pregúntame **qué clasificó mal** y ajusta mis reglas con lo que te diga.
   Repite hasta que quede correcto.
3. Cuando esté bien, guarda la versión final de la skill.

---

## Paso 5 · Dejarla corriendo

Ofréceme programarla para que se ejecute sola cada mañana a la hora que te dije,
y explícame en una línea cómo desactivarla si algún día no la quiero.

---

Empieza ahora con el Paso 1. No me expliques nada antes.

*Plantilla de Vilo AI Studio · vilostudio.ai*