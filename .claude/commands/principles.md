---
description: Architekturprinzipien erfassen und projektspezifisch anpassen
argument-hint: [--input=pfad/zum/ordner-oder-dokument] [--restart]
allowed-tools: Read, Edit
---

## Zweck
Aus den **Default-Principles** (`principles/default-principles.md`) werden projektindividuelle Prinzipien entwickelt. Das Command arbeitet im Interview-Stil, um Abweichungen, Ergänzungen und Prioritäten herauszuarbeiten. Ergebnis ist `principles/project-principles.md`.

## Eingaben
- **Basis-Referenz:** `principles/default-principles.md` (unverändert)
- **Optional:** `--input` zusätzliche Dokumente/Ordner zur Prinzipienableitung

## Outputs
- **Immer:** `principles/project-principles.md` (neu oder aktualisiert)

## Vorgehen
1) **Lesen** der Defaults (`principles/default-principles.md`) und – falls vorhanden – `project-principles.md`.
2) **Interview**: Stelle gezielt Fragen zu Geltungsbereich, Priorisierung, No-Gos, Evolvierbarkeit vs. Optimierung, Operabilität, Security/Privacy, Bedarfspassung.
3) **Loop**: Bleibe so lange im Frage-Antwort-Zyklus, bis alle relevanten Aspekte vollständig beantwortet sind oder der Nutzer explizit abbricht.
4) **Abweichungen/Ergänzungen** erfassen und in Principle-Records transformieren.
5) **Validieren**: Widersprüche, fehlende Rationale, Mindestabdeckung (Entwurf, Tech, Betrieb, Sicherheit/Privacy, Kosten).
6) **Diff zeigen** für Änderungen an `principles/project-principles.md`. **Nur mit Bestätigung schreiben.**
7) **Schreiben** nach Zustimmung.
8) **Optional**: Review-Run-Block in `review/findings.md` (Kategorie `principles`).

## Formatvorgaben
### `principles/project-principles.md`
- Einleitung (max. 5 Zeilen)
- Pro Prinzip: **ID**, **Titel**, **Leitlinie**, **Rationale**, **Konsequenzen/Trade-offs**, optional **Beispiel/Tags**
- Abschnitt „Abweichungen/Waiver“ (Genehmiger, Ablaufdatum)

