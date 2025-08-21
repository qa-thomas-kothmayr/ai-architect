---
description: Architekturoptionen skizzieren und Trade-offs explizit machen
argument-hint: [--input=pfad/zum/ordner-oder-dokument] [--restart] [--export=adr]
allowed-tools: Read, Edit
---

## Zweck
Erarbeitet **2–3 tragfähige Architekturoptionen** auf Basis von **Principles** und **Context** (immer gelesen), ergänzt um Domain und Workload. Macht **Trade-offs**, **Annahmen** und den erwarteten **Entwicklungsaufwand** (nur relativ, keine absoluten Zeitangaben) explizit, bevor Entscheidungen getroffen werden.

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
2) **Optionen vorschlagen (2–3)**
   - Vor automatischen Vorschlägen → Nutzer nach eigenen Ideen fragen.
   - Jede Option = **Architekturstil + Kernbausteine** (z. B. "modulare Monolith→Service-Extraction", "Microservices + Eventing", "CQRS/Event Sourcing" …)
   - Für jede Option automatisch: **Passung** zu Zielen/Workload/Prinzipien, **Annahmen**, **Risiken**, **relativer Entwicklungsaufwand**.
3) **Interview-Loop (ergänzend)**
   - Der Agent stellt **on the fly** Zusatzfragen, bis Optionen **verständlich und vollständig** sind.
   - Typische Klärungen: Datenkonsistenz (stark/schwach), Synch vs. Async, Transaktionsgrenzen, Team-Fit, relative Aufwandsabschätzung.
4) **Vergleich & Trade-offs**
   - Erzeuge Tabelle **Kriterien × Option** mit qualitativer Bewertung (🟢 = gut/hoch, 🟡 = mittel, 🔴 = schlecht/niedrig):
     - Zielerreichung (Top-2 Business/Quality), Evolvierbarkeit, Time-to-Market, Operabilität, Security/Privacy-Fit, Kosten (TCO grob), Entwicklungsaufwand (relativ), Team-Fit, Lock-in-Score.
   - Liste **harte Trade-offs** (z. B. Konsistenz vs. Verfügbarkeit, Latenz vs. Kosten).
5) **Risiken & Spikes**
   - Für jede Option: **Top-3 Risiken** + **Spike-Vorschläge** (Eng umrissene Experimente mit messbaren Beweisen).
6) **Diff zeigen → Schreiben**
   - Änderungen nur nach Bestätigung. Bei `--export=adr`: ADR-Drafts je Option.

## Formatvorgaben
### `design/options.md`
```md
# Architecture Options

## Context Summary
- Ziele/Constraints (Kurz): …
- Workload (Kurz): …
- Prinzipien (Kurz): …

## Options
### Option A – <Titel>
- Stil & Kernidee: …
- Hauptbausteine: …
- Annahmen: …
- Risiken: …
- Entwicklungsaufwand (relativ): 🟢/🟡/🔴 (kurze Begründung)
- Passung zu Zielen/Workload/Prinzipien: ✅/⚠️/❌ (kurze Begründung)

### Option B – <Titel>
…

### Option C – <Titel> (optional)
…

## Trade-offs & Comparison

| Kriterium | Option A | Option B | Option C |
|---|---|---|---|
| Evolvierbarkeit | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Time-to-Market | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Operabilität | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Security/Privacy | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Kosten (TCO grob) | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Entwicklungsaufwand (relativ) | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Team-Fit | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |
| Lock-in-Score (niedriger besser) | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 |

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
* **Vollständigkeit**: Mindestens 2 Optionen; jede mit Annahmen, Risiken, Trade-offs und relativem Entwicklungsaufwand.
* **Transparenz**: Bewertungen sind nachvollziehbar.

## Exit-Kriterien

* `design/options.md` enthält ≥ 2 Optionen mit Vergleich/Trade-offs.
* Relativer Entwicklungsaufwand je Option dokumentiert.
* Offene Risiken mit vorgeschlagenen Spikes dokumentiert.
* (Bei `--export=adr`) ADR-Drafts je Option erzeugt.
