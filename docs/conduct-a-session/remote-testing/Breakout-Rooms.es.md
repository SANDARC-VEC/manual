# Breakout Rooms

Breakout rooms let you split one video conference into separate private rooms, which maps
naturally onto a remote exam session:

- **Main room:** the lobby. Applicants arrive here, are greeted, and wait their turn.
- **One breakout room per applicant under exam:** the applicant plus the three VEs
  observing them. Audio, video, and chat in a breakout room are private to that room, so
  multiple applicants can test simultaneously without disturbing each other.
- **A spare room** is handy for private ID verification or VE-only discussion.

Both Zoom and Google Meet support breakout rooms, but they behave differently in ways
that matter for an exam session. Details for each platform are below.

## Zoom

Zoom's breakout rooms are the more capable of the two: rooms can be pre-built before the
meeting, participants can be locked into their rooms, and hosts can broadcast to every
room at once. See Zoom's
[Managing meeting breakout rooms](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0062540)
for the full reference.

### Before the meeting

Breakout rooms must be enabled for your account before they appear in a meeting. In the
Zoom **web portal** (not the desktop app), go to **Settings → Meeting → In Meeting
(Advanced)** and confirm **Meeting breakout rooms** is on. Enable the
**Assign participants to breakout rooms when scheduling** sub-option if you want to
pre-build rooms.

With that enabled, you can pre-assign rooms while scheduling the meeting: check
**Breakout Room pre-assign** in the meeting options, then either build rooms in the
web portal (add participants by email) or import a CSV using Zoom's template. Limits are
100 rooms and 1,000 pre-assigned participants.

!!! warning "Pre-assignment only works for signed-in Zoom users"
    A pre-assignment only takes effect if the participant joins **signed in to the Zoom
    account matching the email you pre-assigned**. Applicants frequently join from a
    bare meeting link without a Zoom account, so their pre-assignment silently fails and
    they land in the main room. Pre-assignments are also only applied the **first** time
    rooms are opened.

    The reliable pattern: pre-assign only your **VEs** (who can be told to sign in), and
    drag applicants into rooms manually during the session.

### During the meeting

1. Click **Breakout Rooms** in the meeting toolbar.
2. Choose the number of rooms and an assignment mode: **Assign automatically**,
   **Assign manually**, or **Let participants choose room**. For an exam session, choose
   **Assign manually**.
3. Click **Create**. Rooms are built but not opened yet — you can rename rooms
   (e.g. "Exam Room 1") and drag participants in.
4. Click **Open All Rooms** when ready.

While rooms are open, the host and co-hosts can move freely between rooms, move
participants between rooms, and **broadcast a text message or their microphone audio to
every room at once** — useful for announcements like "session ends in 15 minutes."
Participants in a room can click **Ask for Help**, which pings the host to join their
room. Make your VE team co-hosts so they share these controls.

Clicking **Close All Rooms** starts a 60-second countdown visible to everyone, after
which participants return to the main room.

### Recommended Zoom settings for exam sessions

In the breakout rooms **Options** panel (gear icon), change these defaults:

- **Uncheck "Allow participants to choose room"** — applicants go where VEs put them.
- **Uncheck "Allow participants to return to the main session at any time"** — the
  applicant stays in their exam room until the VEs release them; they use **Ask for
  Help** if they need the host.
- **Check "Automatically move all assigned participants into breakout rooms"** — without
  this, each participant must click an invitation to join, which confuses first-timers.
- **Leave "Auto close breakout rooms after X minutes" off** — exams are untimed; a
  countdown timer appearing mid-exam is exactly the distraction you don't want.

In the meeting itself:

- **Enable the Waiting Room** so applicants can be admitted one at a time for check-in.
- **Mute participants upon entry.**
- Set screen sharing to **All Participants** (**Security** menu or **Share Screen**
  arrow → Advanced Sharing Options). Some accounts default to host-only sharing, which
  blocks the applicant screen-share required by the
  [Remote Session Procedures](Remote-Testing.md#remote-session-procedures).

## Google Meet

!!! warning "Breakout rooms require a paid Google Workspace edition"
    Breakout rooms are **not available on free personal Google accounts** or Business
    Starter. The meeting host needs an eligible edition such as Business Standard/Plus,
    Enterprise, Education Plus, the Teaching and Learning Upgrade, or Workspace
    Individual. Anyone (including free accounts) can _join_ a breakout room; only
    creating them is restricted.

    SANDARC maintains a paid account that teams can use to host sessions with Meet
    breakout rooms — contact the VEC at [vec@sandarc.org](mailto:vec@sandarc.org) (see
    [Key Contacts](../../Intro/Key-Contacts.md)) to arrange access.

See Google's
[Use breakout rooms in Google Meet](https://support.google.com/meet/answer/13054147)
host guide for the full reference.

### Before the meeting

Rooms can be pre-built from Google Calendar when creating or editing the event:

1. In the event, click **Add Google Meet video conferencing**, then the gear icon
   (**Change conference settings**).
2. Select **Breakout rooms** in the left menu.
3. Choose the number of rooms (up to 100), then drag invitees into rooms, type names
   directly, or shuffle randomly.
4. Save.

This works well for pre-assigning VEs to their exam rooms. As with Zoom, applicants who
join by link rather than as signed-in invitees will need to be placed manually.

### During the meeting

1. Click the **Meeting tools** button (bottom right), then **Breakout rooms**. This is
   only available to the **meeting host**, and only from a **computer browser** — rooms
   cannot be created or managed from the mobile app.
2. Choose the number of rooms, distribute participants manually or shuffle, and click
   **Open rooms**.

The host can join any room to observe, edit assignments while rooms are open, and click
**End rooms** to bring everyone back. Participants get an **Ask for help** button that
notifies the host. An optional timer can auto-end rooms with a 30-second warning — as
with Zoom, **leave the timer off** for untimed exams.

### Google Meet limitations to plan around

- **Participants can always leave their room.** Meet shows every breakout participant a
  **Return to main call** control and there is no way to lock them in. VEs in each exam
  room must watch that their applicant stays put; an applicant bouncing to the main room
  mid-exam should be treated like any other exam-area violation.
- **There is no broadcast to all rooms.** To make an announcement, visit each room in
  turn or end the rooms.
- **Breakout chat is ephemeral** — messages sent in a room are deleted when the room
  ends, and the host cannot see messages sent while they were not in the room.
- Dial-in phone participants cannot use **Ask for help**, and third-party conferencing
  hardware cannot join breakout rooms at all.

## Zoom vs. Google Meet at a glance

| Capability                         | Zoom                                       | Google Meet                                                                 |
| ---------------------------------- | ------------------------------------------ | --------------------------------------------------------------------------- |
| Pre-build rooms before the meeting | Yes (web portal or CSV) | Yes (Calendar event)                                     |
| Who can manage rooms               | Host and co-hosts                          | Host only, computer browser only                                            |
| Keep applicants in their room      | Yes (option)            | No — participants can always return                                         |
| Broadcast to all rooms             | Yes (text and audio)    | No                                                                          |
| Ask for help button                | Yes                                        | Yes (not for dial-in)                                    |
| Extra cost                         | Included in free and paid plans            | Paid Workspace editions only (SANDARC account available) |
