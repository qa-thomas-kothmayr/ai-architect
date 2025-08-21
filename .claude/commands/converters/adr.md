---
description: Architektur-Entscheidungen als ADRs erzeugen, aktualisieren und superseden
argument-hint: [--input=pfad/zum/ordner-oder-dokument] [--restart] [--non-interactive]
allowed-tools: Read, Edit
---

## Zweck
Legt **Architecture Decision Records (ADRs)** an und hält sie aktuell. Nutzt bestehende **Design-Entscheidungen** und **Principles** als Quelle. Erkennt bereits vorhandene ADRs, ergänzt fehlende, und markiert überholte als **Superseded**.

ADRs werden **toplevel** unter `export/adr/` abgelegt.

## Eingaben (read-only)
- **Immer gelesen:** `design/selections.md`, `principles/project-principles.md`
- **Optional:** `design/*.md`, `context/*.md` (Begründungs- und Verweisgrundlage)
- `--input`: zusätzliche Quellen (z. B. RFCs/Spikes) zur Begründung

## Outputs
- Neue/aktualisierte ADR-Dateien unter `export/adr/ADR-<NNNN>-<slug>.md`
- (Bei Supersede) aktualisierte Header in betroffenen ADRs
- **Sprache:** Deutsch, wenn nicht vom Nutzer anders gefordert
- `export/adr/INDEX.md` (kurzübersicht, Links)

## Aufruf-Logik
- **Erster Aufruf:**
  - scannt `export/adr/` → bestehende ADRs erfassen
  - extrahiert **Entscheidungsthemen** aus `design/selections.md` (Architektur-Option(en), Tech-Kategorien) und ggf. `operability.md`
  - legt ADRs für **fehlende** Themen an, nummeriert fortlaufend
- **Erneuter Aufruf (Default):**
  - legt **nur neue** ADRs an, wenn neue Entscheidungen in den Quellen auftauchen
  - prüft, ob bestehende ADRs durch neue Entscheidungen **superseded** sind → markiert entsprechend
  - erkennt **Minor-Änderungen** (z. B. Präzisierungen) und schlägt Update im selben ADR vor
- **Mit `--restart`:**
  - verschiebt **alle existierenden ADRs** nach `export/adr/<YYYYMMDD-HHMM>/`
  - startet Nummerierung wieder bei `ADR-0001-…`

## Heuristik: Welche ADRs anlegen?
Erzeuge ADRs mindestens für:
- **Gewählte Architektur-Option(en)** (aus `design/selections.md` → „Architecture Style/Option“)
- **Pro Kategorie gewählte Technologie** (Runtime/Framework, Datenhaltung, Messaging, API/Edge, Infra/Orchestration, Observability, Security, CI/CD)
- **Prinzipien-Waiver** (falls in `selections.md` ein Prinzip bewusst verletzt wird)
- **Sicherheits-/Compliance-relevante Entscheidungen** (aus `operability.md`)

## Interview (fokussiert, on the fly)
- Überspringen bei --non-interactive
- Nur wenn Quellen lückenhaft sind: kurze Rückfragen zu **Begründung**, **Konsequenzen**, **Risiken/Mitigation**, **Owner**.
- Keine absoluten Zeitangaben; Aufwand nur **relativ** (🟢/🟡/🔴), falls nötig.

## Nummerierung & Slugs
- Fortlaufende Nummern: `ADR-0001`, `ADR-0002`, … (Lücken nicht neu vergeben)
- `slug` aus Entscheidungsthema in `kebab-case` (z. B. `primary-database-postgres`)

## Supersede-Regeln
- Wenn `design/selections.md` eine frühere Entscheidung **ersetzt**, setze im neuen ADR:
  - `Status: Accepted`
  - `Supersedes: ADR-XXXX: <Titel>`
- und im alten ADR:
  - `Status: Superseded`
  - `Superseded-by: ADR-YYYY: <Titel>`

## Dateiformate
### ADR-Template
liegt in `templates/adr.md`, befülle das Template aber UNBEDINGT AUSFÜHRLICH und NACHVOLLZIEHBAR.

### INDEX.md (automatisch erzeugt/aktualisiert)

```md
# Architecture Decision Records – Index

| ADR | Titel | Status | Datum | Supersedes / By |
|---|---|---|---|---|
| ADR-0001 | Primary database: Postgres | Accepted | 2025-08-21 | - |
| ADR-0002 | Runtime framework: Spring Boot | Accepted | 2025-08-21 | - |
| … | … | … | … | … |
```

## Schreibschutz & Bestätigung

* Zeige **Diff** für neue/aktualisierte ADRs und `INDEX.md`.
* Schreibe nur nach Bestätigung.

## Exit-Kriterien

* `export/adr/` enthält ADRs für alle **entscheidenden** Architektur- und Technologiewahlen aus `design/selections.md`.
* Supersede-Beziehungen sind gesetzt, `INDEX.md` ist konsistent.
* Bei `--restart` wurden alte ADRs in `export/adr/<timestamp>/` verschoben und neues Set generiert.


