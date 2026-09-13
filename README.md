# Meeting Relay simulation

A deterministic, local meeting-note-to-action simulation for the permitted simulated Alexa+ concept. It uses no external APIs, accounts, production data, or Alexa+ services. Extracted actions are always marked `needs_confirmation`; it does not send, create, or change anything. It is an independent simulation, **not an Alexa+ integration or Devpost submission**.

Run:

```bash
python3 -m unittest -v
```

Convert one local UTF-8 meeting note into JSON:

```bash
python3 meeting_relay.py path/to/note.txt
```

The command reads only the supplied local file. Every output action remains `needs_confirmation`.
