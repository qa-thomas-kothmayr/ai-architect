---
description: Architekturoptionen skizzieren und Trade-offs explizit machen
argument-hint: [--input=pfad/zum/ordner-oder-dokument] [--restart] [--export=adr]
allowed-tools: Read, Edit
---

## Zweck
Erarbeitet **2–5 tragfähige Architekturoptionen** auf Basis von **Principles** und **Context** (immer gelesen), ergänzt um Domain und Workload. Generiert **2 konservative** und **1–3 kreative/unkonventionelle** Lösungsansätze. Macht **Trade-offs**, **Annahmen** und den erwarteten **Entwicklungsaufwand** (nur relativ, keine absoluten Zeitangaben) explizit, bevor Entscheidungen getroffen werden.

## Eingaben (read-only)
- `principles/project-principles.md` (immer gelesen)
- `context/context.md`, `context/domain.md`, `context/workload.md` (immer gelesen, falls vorhanden)
- `--input`: Ordner/Dokumente als zusätzliche Quellen (z. B. vorhandene Skizzen); werden als **Initialinput** genutzt

## Outputs
- **Immer:** `design/options.md` (Optionen, Vergleich, Risiken)
- **Optional:** bei `--export=adr` → ADR-Drafts pro Option unter `design/adrs/ADR-xxxx-<option>.md`

## Aufruf-Logik
- **Erster Aufruf:** fragt zunächst, ob der Nutzer eigene Vorschläge für Optionen hat. Danach werden automatisch Vorschläge generiert und im Interview-Loop ergänzt.
- **Erneuter Aufruf:** arbeitet im **Refine-Modus** (Klarstellungen/Updates).
- **Mit `--restart`:** ignoriert bestehende Inhalte und startet neu.

## Vorgehen
1) **Lesen & Ableiten**
   - Extrahiere **Ziele/Constraints** aus Context + Principles.
   - Übernimm **Workload-Klassen (K/M/G/T/0)** und kritische SLOs.

2) **Interview: Nutzer-Optionen erfragen**
   - **Eine einzelne Frage**: "Haben Sie bereits Architekturoptionen im Kopf, die wir berücksichtigen sollen?"
   - Bei Ja: Optionen vom Nutzer sammeln und notieren
   - Bei Nein: Weiter zu Schritt 3

3) **Optionen generieren (2–5)**
   - **2 konservative Optionen**: Bewährte, risikoarme Ansätze (z. B. "modulare Monolith", "klassische 3-Tier", "etablierte Microservices-Patterns")
   - **1–3 kreative/unkonventionelle Optionen**: Innovative, experimentelle oder "out-of-the-box" Ansätze (z. B. "Event Sourcing + CQRS", "Serverless-first", "Actor Model", "Hexagonal + DDD", "Edge Computing", "Blockchain-basiert" je nach Kontext)
   - Jede Option = **Architekturstil + Kernbausteine** mit expliziter Kennzeichnung als "konservativ" oder "kreativ"
   - Für jede Option automatisch: **Passung** zu Zielen/Workload/Prinzipien, **Annahmen**, **Risiken**, **relativer Entwicklungsaufwand**

4) **Interview: Optionen reviewen**
   - **Eine einzelne Frage**: "Hier sind die Optionen [Liste präsentieren]. Möchten Sie einzelne Optionen streichen oder anpassen?"
   - Anpassungen entsprechend vornehmen

5) **Interview-Loop für Details (schrittweise)**
   - **Einzelfragen stellen**, bis alle Optionen **verständlich und vollständig** sind:
     - "Wie wichtig ist starke Datenkonsistenz für Ihr System?" (Option für Option durchgehen)
     - "Bevorzugen Sie synchrone oder asynchrone Kommunikation zwischen Services?"
     - "Wie erfahren ist Ihr Team mit [spezifische Technologie]?"
     - "Welche Transaktionsgrenzen sind für Sie kritisch?"
   - **Pro Frage**: Auf Antwort warten, Implikationen für Optionen anpassen, dann nächste Frage

6) **Vergleich & Trade-offs**
   - Erzeuge Tabelle **Kriterien × Option** mit qualitativer Bewertung (🟢 = gut/hoch, 🟡 = mittel, 🔴 = schlecht/niedrig):
     - Zielerreichung (Top-2 Business/Quality), Evolvierbarkeit, Time-to-Market, Operabilität, Security/Privacy-Fit, Kosten (TCO grob), Entwicklungsaufwand (relativ), Team-Fit, Lock-in-Score
   - Liste **harte Trade-offs** (z. B. Konsistenz vs. Verfügbarkeit, Latenz vs. Kosten)

7) **Risiken & Spikes**
   - Für jede Option: **Top-3 Risiken** + **Spike-Vorschläge** (Eng umrissene Experimente mit messbaren Beweisen)

8) **Diff zeigen → Schreiben**
   - Änderungen nur nach Bestätigung. Bei `--export=adr`: ADR-Drafts je Option

## Formatvorgaben
### `design/options.md`
```md
# Architecture Options

## Context Summary
- Ziele/Constraints (Kurz): …
- Workload (Kurz): …
- Prinzipien (Kurz): …

## Options
### Option A – <Titel> (konservativ)
- Stil & Kernidee: …
- Hauptbausteine: …
- Annahmen: …
- Risiken: …
- Entwicklungsaufwand (relativ): 🟢/🟡/🔴 (kurze Begründung)
- Passung zu Zielen/Workload/Prinzipien: ✅/⚠️/❌ (kurze Begründung)

### Option B – <Titel> (konservativ)
…

### Option C – <Titel> (kreativ)
…

### Option D – <Titel> (kreativ, optional)
…

### Option E – <Titel> (kreativ, optional)
…

## Trade-offs & Comparison

| Kriterium | Option A | Option B | Option C | Option D | Option E |
|---|---|---|---|---|---|
| Evolvierbarkeit | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Time-to-Market | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Operabilität | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Security/Privacy | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Kosten (TCO grob) | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Entwicklungsaufwand (relativ) | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Team-Fit | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Lock-in-Score (niedriger besser) | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |

**Harte Trade-offs**
- …

## Risks & Spikes
- Option A: [R1, R2, R3] → Spike-Vorschläge: …
- Option B: …
- Option C: …
````

### ADR-Template (nur bei `--export=adr`)

```md
# ADR-xxxx: Option <Titel>

## Status
Proposed | {Datum}

## Kontext
Kurzfassung der Ziele/Constraints/Workload/Prinzipien.

## Entscheidung (Option)
Beschreibung der Option, Kernbausteine, Integrationsmuster.

## Begründung
Stärken/Schwächen, Bewertung (🟢/🟡/🔴), harte Trade-offs, Entwicklungsaufwand (relativ).

## Konsequenzen
Implikationen für Teams, Betrieb, Daten; Folgekosten.

## Nächste Schritte
Erforderliche Spikes/Proofs, Messkriterien.
```

## Validierung

* **Konsistenz**: Optionen widersprechen den Prinzipien nicht ohne Waiver.
* **Vollständigkeit**: Mindestens 2 konservative + 1 kreative Option; jede mit Annahmen, Risiken, Trade-offs und relativem Entwicklungsaufwand.
* **Transparenz**: Bewertungen sind nachvollziehbar.

## Exit-Kriterien

* `design/options.md` enthält ≥ 3 Optionen (2 konservativ + ≥1 kreativ) mit Vergleich/Trade-offs.
* Relativer Entwicklungsaufwand je Option dokumentiert.
* Offene Risiken mit vorgeschlagenen Spikes dokumentiert.
* (Bei `--export=adr`) ADR-Drafts je Option erzeugt.
