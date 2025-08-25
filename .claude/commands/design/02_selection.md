---
description: Architektur- und Technologieauswahl konsolidieren und verbindlich festhalten
argument-hint: [--input=pfad/zum/ordner-oder-dokument] [--restart] [--export=adr]
allowed-tools: Read, Edit
---

## Zweck
Konsolidiert **Architektur-Optionen** und **Technologieauswahl** zu einer verbindlichen Entscheidung. Liest **immer** `design/options.md`, `principles/project-principles.md` sowie `context/context.md`/`context/domain.md`/`context/workload.md` (falls vorhanden). Arbeitet im Interview-Stil und dokumentiert das Ergebnis in `design/selections.md`. **Keine absoluten Zeitangaben**, Aufwand nur **relativ** (🟢/🟡/🔴).

## Eingaben (read-only)
- `design/options.md` (immer gelesen)
- `principles/project-principles.md` (immer gelesen)
- `context/*.md` (immer gelesen, falls vorhanden)
- `--input`: Ordner/Dokumente als zusätzliche Quellen (z. B. RFCs, Spike-Ergebnisse)

## Outputs
- **Immer:** `design/selections.md` (gewählte Option(en) + Tech-Stack + Begründung)
- **Optional:** bei `--export=adr` → ADRs für Kernentscheidungen unter `design/adrs/ADR-xxxx-<topic>.md`
- **Zusätzlich:** automatisch "Rejected Alternatives" Abschnitt (aus `design/options.md` übernommen)

## Aufruf-Logik
- **Erster Aufruf:** fragt zuerst, ob eine Option (oder Kombination) bereits favorisiert ist; führt dann Tech-Bewertung durch.
- **Erneuter Aufruf:** **Refine-Modus** – gezielte Klärungen/Updates zu bereits getroffenen Entscheidungen.
- **Mit `--restart`:** ignoriert bestehende Inhalte und startet neu.

## Vorgehen
1) **Lesen & Prüfen**
   - Ziele/Constraints/Workload/Principles laden.
   - Optionen aus `design/options.md` einlesen.
   - **Prinzipien-Check**: markiere Konflikte (⚠️) und verlange Waiver, falls Entscheidung dagegen läuft.

2) **Architektur-Feasibility-Assessment (Interview-Loop, eine Frage pro Schritt)**
   **Für jede Option einzeln und schrittweise durchgehen:**
   
   **Strukturelle Feasibility-Interview:**
   - **Erste Frage**: "Bei Option X - sind klare Service-Boundaries möglich oder entstehen unklare Schnitte?" (Antwort abwarten)
   - **Zweite Frage**: "Gibt es einen schrittweisen Migrations-Pfad oder nur Big Bang?" (Antwort abwarten)
   - **Dritte Frage**: "Ist der Zielzustand klar definiert oder bleibt er vage?" (Antwort abwarten)
   
   **Organisatorische Feasibility-Interview:**
   - **Erste Frage**: "Kann Ihr Team diese Architektur langfristig ownen und weiterentwickeln?" (Antwort abwarten)
   - **Zweite Frage**: "Wäre bei jeder neuen Feature-Anfrage klar, wo sie implementiert wird?" (Antwort abwarten)
   - **Dritte Frage**: "Bleibt die kognitive Komplexität für das Team beherrschbar?" (Antwort abwarten)
   
   **Evolutionäre Feasibility-Interview:**
   - **Erste Frage**: "Können Architektur-Entscheidungen später rückgängig gemacht werden?" (Antwort abwarten)
   - **Zweite Frage**: "Kann das System schrittweise evolvieren?" (Antwort abwarten)
   - **Dritte Frage**: "Sind lokale Optimierungen möglich ohne Gesamtsystem-Refactoring?" (Antwort abwarten)
   
   **Kategorisierung nach Interview:**
   - 🟢 **Obviously Feasible:** Klare Vision, eindeutige Zuordnungen, schrittweise machbar
   - 🟡 **Theoretically Possible, Practically Risky:** Unklare Grenzen, neue Komplexität
   - 🔴 **Obviously Impossible:** Zirkuläre Dependencies, Wildwuchs vorprogrammiert

3) **Optionsauswahl (basierend auf Assessment)**
   - **Entscheidungs-Heuristik:**
     1. Eliminiere alle 🔴 "Obviously Impossible" Optionen
     2. Bevorzuge 🟢 "Obviously Feasible" über 🟡 "Risky"
     3. Bei mehreren 🟢: Wähle die mit geringster Komplexität
     4. Nur wenn keine 🟢: Detaillierte Spike-Analyse für 🟡
   - **Eine einzelne Frage**: "Basierend auf dem Feasibility-Assessment, welche Architektur-Option bevorzugen Sie?"
   - Ergebnis: **gewählte Option(en)** + Feasibility-Begründung; **verworfen**: Feasibility-Kategorie als Grund

4) **Technologieauswahl-Interview (schrittweise pro Kategorie)**
   - **Kategorien-Bestimmung**: "Welche Technologie-Kategorien sind für Ihr Projekt relevant?" (Beispiele zeigen: Runtime/Framework, Datenhaltung, Messaging/Integration, API/Edge, Infra/Orchestration, Observability, Security, CI/CD)
   - **Pro Kategorie einzeln durchgehen:**
     - **Schritt 1**: "Für Kategorie X - welche 2-4 Kandidaten sollen wir betrachten?" (Antwort abwarten)
     - **Schritt 2**: "Wie wichtig ist für Sie [Kriterium Y] bei dieser Auswahl?" (pro Kriterium einzeln fragen)
     - **Schritt 3**: Bewertungsmatrix mit Ampel erstellen (🟢 gut/hoch, 🟡 mittel, 🔴 schlecht/niedrig)
     - **Schritt 4**: "Basierend auf der Bewertung - welcher Kandidat für Kategorie X?"
   - **Zusatzfragen einzeln bei Bedarf**: 
     - "Welche Erfahrung hat Ihr Team mit [Technologie]?"
     - "Gibt es Compliance-Anforderungen für [Kategorie]?"
     - "Bestehen Hosting-Vorgaben?"

5) **Konsolidierung & Entscheidung**
   - **Entscheidungspaket** erzeugen: gewählte Option(en) + je Kategorie der gewählte Technologie-Kandidat.
   - **Begründung** pro Wahl (1–3 Sätze) + **Risiken & Mitigation** (Stichpunkte).
   - **Waiver** erzeugen, wenn Prinzipienkonflikt bewusst akzeptiert wird (mit Ablaufdatum/Owner).

6) **Diff zeigen → Schreiben**
   - Änderungen an `design/selections.md` nur nach Bestätigung schreiben. Bei `--export=adr`: ADRs generieren.

## Formatvorgaben
### `design/selections.md`
```md
# Architecture & Technology Selections

## Summary
- Gewählte Option(en): …
- Feasibility-Kategorie: 🟢/🟡/🔴
- Kerngründe: …
- Haupt-Risiken & Mitigations: …

## Feasibility Assessment

### Option A: [Name]
- **Strukturelle Feasibility:** [Bewertung mit Begründung]
- **Organisatorische Feasibility:** [Bewertung mit Begründung]
- **Evolutionäre Feasibility:** [Bewertung mit Begründung]
- **Gesamtbewertung:** 🟢/🟡/🔴

### Option B: [Name]
[gleiche Struktur]

## Selected Architecture
- Option(en): … (basierend auf Feasibility-Assessment)
- Abhängigkeiten/Impakts: …

## Technology Matrix (Ampelbewertung)
### Kategorie: <z. B. Datenhaltung>
| Kriterium | Postgres | DynamoDB | … |
|---|:---:|:---:|:---:|
| Zielerreichung | 🟢 | 🟢 | … |
| Evolvierbarkeit | 🟢 | 🟡 | … |
| Time-to-Market | 🟢 | 🟡 | … |
| Operabilität | 🟢 | 🟢 | … |
| Security/Privacy | 🟡 | 🟢 | … |
| Kosten (TCO) | 🟢 | 🟡 | … |
| Aufwand (relativ) | 🟢 | 🟡 | … |
| Team-Fit | 🟢 | 🟡 | … |
| Lock-in | 🟢 | 🔴 | … |

### Kategorie: <z. B. Runtime/Framework>
| Kriterium | Spring Boot | Node/NestJS | … |
|---|:---:|:---:|:---:|
| Zielerreichung | 🟢 | 🟡 | … |
| Evolvierbarkeit | 🟢 | 🟡 | … |
| Time-to-Market | 🟢 | 🟢 | … |
| Operabilität | 🟢 | 🟡 | … |
| Security/Privacy | 🟡 | 🟡 | … |
| Kosten (TCO) | 🟡 | 🟢 | … |
| Aufwand (relativ) | 🟡 | 🟡 | … |
| Team-Fit | 🟢 | 🟢 | … |
| Lock-in | 🟡 | 🟡 | … |

## Decision & Rationale
- Architektur-Entscheidung: … (Warum diese, warum nicht die anderen)
- Technologie-Entscheidungen je Kategorie: …
- Prinzipienkonflikte & Waiver: …

## Rejected Alternatives
- Option B: … (kurz)
- Kandidat X (Kategorie Y): … (kurz)

## Folgen & nächste Schritte
- Spikes/Proofs zur Risikoreduktion: …
- Migrations-/Einführungsplan (nur grob, relativ): …
````

### ADR-Template (optional via `--export=adr`)

```md
# ADR-xxxx: <Entscheidungsthema>

## Status
Accepted | {Datum}

## Kontext
Kurzfassung aus Options, Principles & Context.

## Entscheidung
- Gewählte Option(en) und Techs.

## Begründung
- Ampel-Resümee je Hauptkriterium (🟢/🟡/🔴), Schlüsselfaktoren.

## Konsequenzen
- Auswirkungen auf Betrieb, Daten, Teams, Kosten.

## Risiken & Mitigation
- R1: … / Mitigation: …
- R2: … / Mitigation: …

## Waiver (falls nötig)
- Prinzipienkonflikt: … / Gültig bis: … / Owner: …
```

## Validierung

* **Feasibility-Assessment**: Alle Optionen kategorisiert (🟢/🟡/🔴) mit Begründung.
* **Prinzipien-Treue**: Keine verdeckten Konflikte; Waiver falls nötig.
* **Nachvollziehbarkeit**: Jede Auswahl hat kurze Begründung basierend auf Feasibility.
* **Vollständigkeit**: Architektur + Tech-Kategorien sind entschieden oder bewusst offen (mit TODO/Spike).

## Exit-Kriterien

* `design/selections.md` existiert mit Feasibility-Assessment für alle Optionen.
* Gewählte Architektur basiert auf Feasibility-Kategorisierung (🟢 > 🟡 > 🔴).
* Verworfene Optionen/Kandidaten sind mit Feasibility-Grund dokumentiert.
* (Bei `--export=adr`) ADRs für Kernentscheidungen erstellt.
