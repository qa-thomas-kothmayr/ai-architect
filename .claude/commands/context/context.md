---
description: Projekt-Kontext, Stakeholder, Ziele und Einschränkungen erfassen
argument-hint: [--input=pfad/zum/ordner-oder-dokument] [--restart]
allowed-tools: Read, Edit
---

## Zweck
Erfasst im Interview-Stil die **Projektumgebung**: Stakeholder, Geschäftsziele, Qualitätsziele, Einschränkungen. Ergebnisse landen in `context/context.md`.

## Eingaben
- **Optional (read-only):**
  - `principles/project-principles.md` (um Haltung & Prinzipien zu spiegeln)
  - Bereits vorhandene `context/context.md` (wenn vorhanden) oder ein vom Nutzer per `--input` angegebener Ordner/Dokumentpfad als Initialinput.
- **Hinweis:**
  - Falls Inputdatei/ordner existiert, als Basis verwenden und im Interview gezielt um Klarstellung/Ergänzung bitten.
  - Bei erneutem Aufruf ist der **Default-Modus**: **Klärungen oder Updates** zu bestehenden Punkten ermöglichen.
  - Mit `--restart` wird die Datei komplett neu aufgebaut und alle vorherigen Inhalte überschrieben.

## Outputs
- **Immer:** `context/context.md`

## Interview-Loop
Führe die folgenden Blöcke **sequenziell** aus. **Bleibe im Frage-Antwort-Zyklus**, bis alle relevanten Aspekte beantwortet, verständlich und vollständig sind oder der Nutzer explizit abbricht. 
- Der Agent darf **on the fly zusätzliche Fragen** stellen, wenn Unklarheiten entstehen oder Kontext fehlt.
- Wenn eine Datei oder ein Ordner als Input angegeben ist, nutze deren Inhalte als Startpunkt und bitte gezielt um Präzisierungen.

### 1) Stakeholder
- Wer sind die **primären Stakeholder** (Entscheider, Nutzer)?
- Wer sind die **sekundären Stakeholder** (Betreiber, Nachbarsysteme, Support)?
- Gibt es externe Stakeholder (Regulatoren, Partner)? [J/N] → bei J: bitte auflisten.
- Falls Input vorhanden: Stimmen die gelisteten Stakeholder? Was fehlt?

### 2) Geschäftsziele
- Was ist das **Hauptziel** des Projekts?
- Gibt es weitere **Business-Goals** (z. B. Kostenersparnis, Geschwindigkeit, Marktposition)?
- Priorisierung: Welche 1–2 Ziele sind **absolut kritisch**?
- Falls Input vorhanden: Stimmen die formulierten Ziele? Was präzisieren?

### 3) Qualitätsziele
- Welche **nicht-funktionalen Anforderungen** sind wichtig? (Beispiele: Sicherheit, Performance, Time-to-Market, Wartbarkeit, Erweiterbarkeit, Compliance)
- Welche 1–2 Qualitätsziele haben **höchste Priorität**?
- Müssen Standards/Normen erfüllt werden? [J/N] → bei J: welche?
- Falls Input vorhanden: Stimmen die aufgelisteten Qualitätsziele? Was fehlt?

### 4) Einschränkungen (Constraints)
- Gibt es vorgegebene **Technologien/Stacks**? [J/N] → bei J: welche?
- Gibt es **organisatorische Restriktionen** (Budget, Ressourcen, Zeit)? [J/N] → bei J: welche?
- Gibt es **rechtliche/Compliance-Vorgaben**? [J/N] → bei J: welche?
- Gibt es bestehende **Integrations- oder Betriebs-Constraints** (Hosting, Cloud-Provider, Ops-Vorgaben)? [J/N] → bei J: welche?
- Falls Input vorhanden: Stimmen die Constraints? Müssen sie geschärft werden?

## Transformation → `context/context.md`
Nach dem Interview generiere:
- **Summary** (kurz, stichpunktartig)
- **Details** (gegliedert in Stakeholder, Business Goals, Quality Goals, Constraints)
- **Annahmen & Quellen** (mit Datum)

Beispielstruktur:
```md
# Project Context

## Summary
- Stakeholder: …
- Business Goals: …
- Quality Goals: …
- Constraints: …

## Details
### Stakeholder
…

### Business Goals
…

### Quality Goals
…

### Constraints
…

## Annahmen & Quellen
- …
