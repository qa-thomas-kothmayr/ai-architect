---
description: Architektur-Artefakte prüfen – Konsistenz, Vollständigkeit, Prinzipien-Check
argument-hint: [--input=pfad/zum/ordner-oder-dokument] [--severity=all|major] [--restart]
allowed-tools: Read, Edit
---

## Zweck
Prüft Architektur-Artefakte auf **Konsistenz**, **Vollständigkeit** und **Prinzipien-Konformität**.
- **Default ohne --input:** gesamtes Set prüfen (Principles, Context, Domain, Workload, Options, Selections, Structure, Operability).
- **Mit --input:** nur angegebene Datei(en)/Ordner prüfen (kann mehrfach angegeben werden).
- Ergebnis wird als **zeitgestempeltes Review-Dokument** unter `review/YYYYMMDD-HHMM-review.md` abgelegt (nur nach Bestätigung).

## Eingaben (read-only)
- **Immer gelesen:** `principles/project-principles.md`
- Zusätzlich (falls vorhanden): `context/*.md`, `design/*.md`
- `--input`: Pfade zu spezifischen Artefakten/Ordnern (optional, mehrfach)

## Outputs
- `review/<timestamp>-review.md` (z. B. `review/20250821-1530-review.md`)

## Aufruf-Logik
- **Erster Aufruf:** erstellt frisches Review basierend auf Auswahl/Default.
- **Erneuter Aufruf:** **Refine-Modus** – ergänzt den letzten Reviewlauf um Updates/Statusänderungen.
- `--severity=major` zeigt nur schwere Findings (Blocker/High); Default `all`.

## Prüfblöcke
Der Agent führt folgende Checks aus und sammelt Findings (mit **Severity** 🟥 High / 🟧 Medium / 🟨 Low):

1) **Prinzipien-Alignment**
- Widersprüche zwischen Entscheidungen/Struktur und `project-principles.md` → Waiver nötig?

2) **Kontext-Kohärenz**
- Ziele/Constraints aus `context/context.md` konsistent in Options/Selections/Structure/Operability gespiegelt?

3) **Workload-Fit**
- Lastannahmen (K/M/G/T, RPH, Events/Day) ↔ Struktur/Operability (Skalierung, Caching, Datenpfade) stimmig?

4) **Domain/Scope-Deckung**
- `domain.md` Bounded Contexts ↔ Struktur-Schnitt; fehlende/überlappende Verantwortlichkeiten?

5) **Options ↔ Selections**
- Verworfen/gewählt konsistent dokumentiert? Trade-offs im Selection-Text reflektiert?

6) **Struktur-Qualität**
- Schnittstellen-Tabelle vollständig (Richtung/Protokoll/Format/Frequenz)?
- Sequenzen vorhanden und mit Struktur konsistent? Mermaid-Syntax validierbar?

7) **Operability/NFRs**
- SLI/SLOs klar (messbar)? Verfügbarkeit/Recovery/Observability/Security hinreichend?
- Risiken/Measures dokumentiert; MUST/SHOULD priorisiert?

8) **Security & Privacy**
- AuthN/Z, Datenklassifikation, Verschlüsselung, DSGVO-relevante Flows, Logging/PII?

9) **Risiken & Kosten**
- Explizite Risiken, Lock-in, grobe Kosten-/Aufwandsimplikationen (relativ) vorhanden?

10) **Vollständigkeit & Nachverfolgbarkeit**
- Alle Artefakte vorhanden? Querverweise & Quellen/Annahmen sauber?

## Interview-Loop (fokussiert)
- Der Agent stellt **nur bei kritischen Unklarheiten** Rückfragen (on the fly), um Fehlalarme zu vermeiden.
- Bei klaren Abweichungen werden **konkrete Änderungsvorschläge** vorbereitet (Diff/Patche) – Schreiben erst nach Bestätigung.

## Ausgabeformat
### `review/<timestamp>-review.md`
```md
# Architecture Review – <YYYY-MM-DD HH:MM>

## Scope
Geprüft: <Liste der Dateien/Ordner oder „Gesamtes Set“>

## Summary
- Stärken: …
- Wichtigste Risiken: …
- Blocker (falls vorhanden): …

## Findings
### [🟥/🟧/🟨] <Kurz-Titel>
- **Kategorie:** Prinzipien | Kontext | Workload | Domain | Options/Selections | Struktur | Operability | Security/Privacy | Kosten/Aufwand | Sonstiges
- **Beschreibung:** …
- **Beleg/Quelle:** … (Zeilen/Abschnitte referenzieren)
- **Vorschlag:** … (konkrete Änderung oder Frage)
- **Status:** Open | Accepted | Rejected | Fixed (mit Datum)
- **Owner:** … (falls benannt)

… (weitere Findings)

## Follow-ups
- TODOs/Spikes mit kurzer Zieldefinition
- Nächster Reviewpunkt (optional)
```

## Validierung

* **Trennschärfe:** Findings sind nachvollziehbar, referenziert und einer Kategorie zugeordnet.
* **Relevanz:** Bei `--severity=major` nur 🟥/🟧.
* **Umsetzbarkeit:** Jeder Vorschlag ist konkret oder als präzise Frage formuliert.

## Exit-Kriterien

* Zeitgestempeltes Review-Dokument unter `review/` erzeugt und bestätigt.
* Blocker (🟥) sind klar benannt oder explizit als Waiver dokumentiert.

