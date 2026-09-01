# Salas para grupos pequeños

Las salas para grupos pequeños permiten dividir una videoconferencia en salas privadas
independientes, algo que se adapta de forma natural a una sesión de examen remota:

- **Sala principal:** la sala de espera. Los aspirantes llegan aquí, se les da la bienvenida y esperan su turno.
- **Una sala para grupos pequeños por cada aspirante que se examina:** el aspirante más los tres VE
  que lo supervisan. El audio, el vídeo y el chat de una sala para grupos pequeños son privados de esa sala, por lo que
  varios aspirantes pueden examinarse simultáneamente sin molestarse entre sí.
- **Una sala de reserva** resulta útil para verificar la identidad en privado o para conversaciones solo entre VE.

Tanto Zoom como Google Meet admiten salas para grupos pequeños, pero se comportan de forma distinta
en aspectos que resultan importantes para una sesión de examen. A continuación se ofrecen los detalles de cada plataforma.

## Zoom

Las salas para grupos pequeños de Zoom son las más completas de las dos: las salas se pueden crear antes de la
reunión, se puede impedir que los participantes salgan de su sala y los anfitriones pueden transmitir un mensaje a todas
las salas a la vez. Consulta el artículo de Zoom
[Gestión de las salas para grupos pequeños de la reunión](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0062540)
para ver la referencia completa.

### Antes de la reunión

Las salas para grupos pequeños deben estar habilitadas en tu cuenta para que aparezcan en una reunión. In the
Zoom **web portal** (not the desktop app), go to **Settings → Meeting → In Meeting
(Advanced)** and confirm **Meeting breakout rooms** is on. Enable the
**Assign participants to breakout rooms when scheduling** sub-option if you want to
pre-build rooms.

With that enabled, you can pre-assign rooms while scheduling the meeting: check
**Breakout Room pre-assign** in the meeting options, then either build rooms in the
web portal (add participants by email) or import a CSV using Zoom's template. Los límites son
100 salas y 1.000 participantes asignados previamente.

!!! warning "La asignación previa solo funciona con usuarios de Zoom que hayan iniciado sesión"
    Una asignación previa solo surte efecto si el participante se une **con la sesión iniciada en la cuenta
    de Zoom que corresponde al correo electrónico que asignaste previamente**. Los aspirantes suelen unirse desde
    un simple enlace a la reunión, sin cuenta de Zoom, por lo que su asignación previa falla sin avisar y
    acaban en la sala principal. Además, las asignaciones previas solo se aplican la **primera** vez
    que se abren las salas.

    The reliable pattern: pre-assign only your **VEs** (who can be told to sign in), and
    drag applicants into rooms manually during the session.

### Durante la reunión

1. Click **Breakout Rooms** in the meeting toolbar.
2. Choose the number of rooms and an assignment mode: **Assign automatically**,
   **Assign manually**, or **Let participants choose room**. For an exam session, choose
   **Assign manually**.
3. Click **Create**. Las salas quedan creadas pero aún no abiertas: puedes cambiarles el nombre
   (p. ej., «Sala de examen 1») y arrastrar participantes a ellas.
4. Click **Open All Rooms** when ready.

Mientras las salas están abiertas, el anfitrión y los coanfitriones pueden moverse libremente entre salas, mover
participantes de una sala a otra y **transmitir un mensaje de texto o el audio de su micrófono a
todas las salas a la vez**, algo útil para anuncios como «la sesión termina en 15 minutos».
Los participantes de una sala pueden hacer clic en **Pedir ayuda**, lo que avisa al anfitrión para que se una a su
sala. Make your VE team co-hosts so they share these controls.

Al hacer clic en **Cerrar todas las salas** se inicia una cuenta atrás de 60 segundos visible para todos, tras
la cual los participantes vuelven a la sala principal.

### Configuración de Zoom recomendada para las sesiones de examen

In the breakout rooms **Options** panel (gear icon), change these defaults:

- **Uncheck "Allow participants to choose room"** — applicants go where VEs put them.
- **Uncheck "Allow participants to return to the main session at any time"** — the
  applicant stays in their exam room until the VEs release them; they use **Ask for
  Help** if they need the host.
- **Check "Automatically move all assigned participants into breakout rooms"** — without
  this, each participant must click an invitation to join, which confuses first-timers.
- **Leave "Auto close breakout rooms after X minutes" off** — exams are untimed; a
  countdown timer appearing mid-exam is exactly the distraction you don't want.

En la propia reunión:

- **Enable the Waiting Room** so applicants can be admitted one at a time for check-in.
- **Mute participants upon entry.**
- Set screen sharing to **All Participants** (**Security** menu or **Share Screen**
  arrow → Advanced Sharing Options). Algunas cuentas tienen configurado de forma predeterminada que solo el anfitrión pueda compartir, lo que
  impide que el aspirante comparta su pantalla, tal como exigen los
  [Procedimientos de sesión remota](Remote-Testing.md#remote-session-procedures).

## Google Meet

!!! warning "Las salas para grupos pequeños requieren una edición de pago de Google Workspace"
    Las salas para grupos pequeños **no están disponibles en las cuentas personales gratuitas de Google** ni en Business
    Starter. El anfitrión de la reunión necesita una edición válida, como Business Standard/Plus,
    Enterprise, Education Plus, la Actualización para la Enseñanza y el Aprendizaje o Workspace
    Individual. Cualquier persona (incluidas las cuentas gratuitas) puede _unirse_ a una sala para grupos pequeños; la restricción
    afecta únicamente a su creación.

    SANDARC mantiene una cuenta de pago que los equipos pueden usar para organizar sesiones con
    salas para grupos pequeños de Meet: comunícate con el VEC en [vec@sandarc.org](mailto:vec@sandarc.org) (consulta
    [Contactos clave](../../Intro/Key-Contacts.md)) para coordinar el acceso.

Consulta la guía para anfitriones de Google
[Usar salas para grupos pequeños en Google Meet](https://support.google.com/meet/answer/13054147)
para obtener la referencia completa.

### Antes de la reunión

Las salas se pueden crear con antelación desde Google Calendar al crear o editar el evento:

1. In the event, click **Add Google Meet video conferencing**, then the gear icon
   (**Change conference settings**).
2. Selecciona **Salas para grupos pequeños** en el menú de la izquierda.
3. Elige la cantidad de salas (hasta 100) y luego arrastra a los invitados a las salas, escribe los nombres
   directamente o distribúyelos de forma aleatoria.
4. Save.

Esto funciona muy bien para asignar previamente a los VE a sus salas de examen. Al igual que en Zoom, los aspirantes que
se unan mediante el enlace en lugar de hacerlo como invitados con sesión iniciada deberán colocarse manualmente.

### Durante la reunión

1. Click the **Meeting tools** button (bottom right), then **Breakout rooms**. Esto
   solo está disponible para el **anfitrión de la reunión** y únicamente desde un **navegador de computadora**: las salas
   no se pueden crear ni administrar desde la app para dispositivos móviles.
2. Choose the number of rooms, distribute participants manually or shuffle, and click
   **Open rooms**.

El anfitrión puede unirse a cualquier sala para observar, editar las asignaciones mientras las salas están abiertas y hacer clic
en **Finalizar salas** para que todos regresen. Los participantes disponen de un botón **Pedir ayuda** que
avisa al anfitrión. Un temporizador opcional puede cerrar las salas automáticamente con un aviso de 30 segundos; al igual
que en Zoom, **deja el temporizador desactivado** para los exámenes sin límite de tiempo.

### Limitaciones de Google Meet que hay que tener en cuenta

- **Los participantes siempre pueden salir de su sala.** Meet muestra a todos los participantes de una sala un
  control **Volver a la llamada principal** y no hay forma de impedírselo. Los VE de cada sala de
  examen deben vigilar que su aspirante permanezca allí; un aspirante que salte a la sala principal
  en mitad del examen debe tratarse como cualquier otra infracción del área de examen.
- **No hay difusión a todas las salas.** Para hacer un anuncio, visita cada sala por
  turno o finaliza las salas.
- **El chat de las salas es efímero**: los mensajes enviados en una sala se eliminan cuando esta
  finaliza, y el anfitrión no puede ver los mensajes enviados mientras no estaba en la sala.
- Los participantes que se conectan por teléfono no pueden usar **Pedir ayuda**, y el hardware de
  videoconferencia de terceros no puede unirse en absoluto a las salas para grupos pequeños.

## Zoom frente a Google Meet de un vistazo

| Función                              | Zoom                                       | Google Meet                                                                                          |
| ------------------------------------ | ------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Crear las salas antes de la reunión  | Sí (portal web o CSV)   | Sí (evento de Calendar)                                                           |
| Quién puede administrar las salas    | Anfitrión y coanfitriones                  | Solo el anfitrión, y solo desde un navegador de computadora                                          |
| Mantener a los aspirantes en su sala | Sí (opción)             | No: los participantes siempre pueden volver                                          |
| Difusión a todas las salas           | Sí (texto y audio)      | No                                                                                                   |
| Botón Pedir ayuda                    | Sí                                         | Sí (no para conexiones telefónicas)                                               |
| Costo adicional                      | Incluido en los planes gratuitos y de pago | Solo en las ediciones de pago de Workspace (hay una cuenta de SANDARC disponible) |
