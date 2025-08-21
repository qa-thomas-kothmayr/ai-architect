---
description: Projekt-Domain & Scope erfassen – artefaktbasiert entdecken mit gezielten Rückfragen
argument-hint: [--input=pfad/zum/ordner-oder-dokument] [--restart]
allowed-tools: Read, Edit
---

## Zweck
**Artefaktgestützt plus Interview.** Der Agent **erkennt zunächst automatisch Kandidaten** für Scope, Bounded Contexts und Schnittstellen aus vorhandenen Artefakten und bittet dich anschließend um **gezielte Bestätigungen und Ergänzungen**. Dadurch wird das Grundgerüst automatisch erstellt, aber wichtige Feinheiten werden im Dialog abgeklärt.

## Aufruf-Logik
- **Erster Aufruf (ohne Parameter):** führt immer eine **Discovery** durch und zeigt Kandidaten zur Bestätigung an.
- **Erneuter Aufruf:** arbeitet im **Refine-Modus**, d. h. stellt gezielte Fragen zu bestehenden Inhalten und ermöglicht Updates/Korrekturen.
- **Mit `--restart`:** ignoriert bestehende Inhalte und startet die Discovery von vorne.

## Eingaben (Read-only)
- `context/*.md` (Ziele/Constraints/Workload) – falls vorhanden
- `principles/project-principles.md` – optional, zur Haltung
- `--input` Ordner/Datei(en) als Quellen; falls nicht gesetzt: Standardquellen im Repo scannen (OpenAPI/GraphQL/Proto, SQL-Schema, Markdown-Doku, Pipelines, Module)

## Outputs
- **Immer:** `context/domain.md` (nach Bestätigung)
- **Zusätzlich:**
  - `context/domain-candidates.md` (Entdeckte Kandidaten mit Begründungen & Confidence)
  - `context/glossary.md` (extrahierte Domänenbegriffe + erste Definitionen)
  - `context/integrations.md` (externe Systeme & Schnittstellen-Inventar)

## Discovery (automatisch)
Extraktion von:
- **Capabilities** (aus APIs, Modulen, Struktur)
- **Entities/Aggregate** (aus Schema, Typen)
- **Events** (aus Topics/Queues)
- **Integrationen** (externe Endpunkte, Pipelines)
- **Kopplung** (Import/DependsOn, Änderungsrate)

Kandidatenliste: Context A/B/… mit Entities, Capabilities, Events, Integrationen, Confidence & Rationale.

## Interview-Loop
Nach der Discovery beginnt ein **ergänzendes Interview**:
- **Scope**: Passt die Abgrenzung? Gibt es fachliche Themen, die fehlen oder explizit ausgeschlossen sind?
- **Bounded Contexts**: Stimmen die Vorschläge? Müssen welche zusammengelegt oder aufgeteilt werden? Gibt es weitere, die nicht erkannt wurden?
- **Integrationen & Schnittstellen**: Fehlt eine externe Verbindung? Welche Schnittstellen sind kritisch oder besonders stabil/instabil?
- **Domänenbegriffe**: Gibt es zentrale Begriffe/Ubiquitous Language, die unbedingt dokumentiert werden sollen?
- **Policies & Regeln**: Gibt es 1–3 zentrale fachliche Regeln, die als Querschnitt gelten? (z. B. Datenschutz, regulatorische Regeln)

Der Agent darf **on the fly Zusatzfragen** stellen, wenn Unklarheiten auftauchen.

## Datei-Struktur & Inhalte
### `context/domain-candidates.md`
- Liste der Kandidaten (Name, Kurzbeschreibung, Entities/Capabilities/Events, Integrationen, Confidence, Rationale)
- Vorschläge für Merge/Split (mit Begründung)

### `context/domain.md`
```md
# Project Domain

## Summary
- Scope: …
- Bounded Contexts: …
- Schnittstellen: …
- Policies & Language: …

## Details
### Scope
…

### Bounded Contexts (final)
- <Name>: Zweck, Hauptentitäten, Haupt-Use-Cases, Integrationen
…

### Schnittstellen & Externe Systeme
…

### Fachliche Regeln & Policies
…

## Annahmen, Quellen & Confidence
- Quelle A … (Confidence: hoch/mittel/niedrig)
- …
```

## Validierung & Writes

1. **Validieren**: Konsistenz und Ownership prüfen
2. **Diff anzeigen** (Candidates → Domain final, Diagramme)
3. **Nur nach Bestätigung schreiben**

## Exit-Kriterien

* `context/domain.md` existiert mit finaler Context-Liste & Scope
* `context/diagrams/context-map.md` erzeugt und konsistent
* Quellen & Confidence dokumentiert
