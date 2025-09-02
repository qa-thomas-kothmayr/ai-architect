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
- **Sprache:** Ausschließlich Deutsch (alle Inhalte, Metadaten, Status-Bezeichnungen)
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
  - verschiebt **alle existierenden ADRs** nach `export/backup-YYYYMMDD-HHMMSS/adr/` (einheitliches Backup-Format)
  - erstellt METADATA.md mit Backup-Informationen
  - startet Nummerierung wieder bei `ADR-0001-…`

## Heuristik: Welche ADRs anlegen?
Erzeuge ADRs mindestens für:
- **Gewählte Architektur-Option(en)** (aus `design/selections.md` → „Architecture Style/Option“)
- **Pro Kategorie gewählte Technologie** (Runtime/Framework, Datenhaltung, Messaging, API/Edge, Infra/Orchestration, Observability, Security, CI/CD)
- **Prinzipien-Waiver** (falls in `selections.md` ein Prinzip bewusst verletzt wird)
- **Sicherheits-/Compliance-relevante Entscheidungen** (aus `operability.md`)

## Content Quality Standards
- **Decision clarity**: Klare "Was wird entschieden", "Warum diese Option", "Welche Alternativen" Struktur
- **Developer-friendly language**: Technische Begründungen mit Business-Kontext
- **Practical examples**: Code-Snippets, Konfiguration, konkrete Implementierungshinweise  
- **Cross-referencing**: Verweise zu verwandten ADRs, Principles, Design-Dokumenten
- **Visual organization**: Tabellen für Alternative-Vergleiche, Listen für Konsequenzen
- **Terminology consistency**: Einheitliche Begriffe mit anderen Architektur-Dokumenten
- **Context provision**: Geschäftskontext und Stakeholder-Impact erklären

## Interview (fokussiert, on the fly)
- Überspringen bei --non-interactive
- Nur wenn Quellen lückenhaft sind: kurze Rückfragen zu **Begründung**, **Konsequenzen**, **Risiken/Mitigation**, **Owner**.
- Keine absoluten Zeitangaben; Aufwand nur **relativ** (🟢/🟡/🔴), falls nötig.

## Nummerierung & Slugs
- Fortlaufende Nummern: `ADR-0001`, `ADR-0002`, … (Lücken nicht neu vergeben)
- `slug` aus Entscheidungsthema in `kebab-case` (z. B. `primary-database-postgres`)

## Einheitliche Metadaten-Standards
- **Timestamp-Format**: ISO 8601 (YYYY-MM-DD HH:MM:SS)
- **Agent-Referenz**: Claude Code v{version} + Command-Name
- **Source-Tracking**: Vollständige Pfade zu genutzten Design-Dokumenten
- **Change-Log**: Kurze Beschreibung der Änderungen seit letztem Export
- **Status-Werte**: Ausschließlich deutsch ("Akzeptiert", "Abgelehnt", "Überholt", "Vorgeschlagen")

## Supersede-Regeln
- Wenn `design/selections.md` eine frühere Entscheidung **ersetzt**, setze im neuen ADR:
  - `Status: Akzeptiert`
  - `Ersetzt: ADR-XXXX: <Titel>`
- und im alten ADR:
  - `Status: Überholt`
  - `Überholt-durch: ADR-YYYY: <Titel>`

## Template Structure Enhancement
- **Template-Validierung**: Prüfe `templates/adr.md` auf Vollständigkeit vor ADR-Erstellung
- **Beispiel-Content**: Template mit Muster-Inhalten als Leitfaden für ADR-Generierung
- **Validierung-Marker**: Kennzeichnung von Pflicht- vs. optionalen ADR-Abschnitten
- **Cross-Reference-Templates**: Vordefinierte Verknüpfungsstrukturen zu Design-Dokumenten
- **Quality Gates**: Mindest-Inhaltslänge und erforderliche Begründungstiefe
- **Smart Fallbacks**: Nur bei kritischen fehlenden Entscheidungsgrundlagen nachfragen
- **Completeness Checks**: Markiere unvollständige ADR-Abschnitte für spätere Ergänzung (⚠️ NEEDS REVIEW)

## Dateiformate
### ADR-Template Structure
liegt in `templates/adr.md`, befülle das Template mit folgenden Quality Gates:

**Pflicht-Abschnitte**:
- **Titel** (PFLICHT): Präzise Beschreibung der Entscheidung
- **Status** (PFLICHT): Akzeptiert/Vorgeschlagen/Überholt/Abgelehnt
- **Kontext** (PFLICHT, min. 100 Wörter): Geschäfts- und technischer Hintergrund
- **Entscheidung** (PFLICHT, min. 150 Wörter): Was wird entschieden und warum
- **Konsequenzen** (PFLICHT): Positive/negative Auswirkungen

**Cross-References** (PFLICHT):
- `→ Implementiert Prinzip: [Prinzip X](../principles/project-principles.md#prinzip-x)`
- `→ Bezug zu Selections: [Design Selections](../design/selections.md)`
- `→ Verwandte ADRs: [ADR-XXXX](ADR-XXXX-titel.md)`

**Quality Gates pro ADR**:
- ✅ Mindestens 3 alternative Optionen betrachtet
- ✅ Mindestens 2 positive und 2 negative Konsequenzen
- ✅ Klare Business-Begründung vorhanden
- ✅ Mindestens 1 Cross-Reference zu Design-Dokumenten

### INDEX.md (automatisch erzeugt/aktualisiert)

```md
# Architecture Decision Records – Index

| ADR | Titel | Status | Datum | Ersetzt / Überholt-durch |
|---|---|---|---|---|
| ADR-0001 | Primäre Datenbank: Postgres | Akzeptiert | 2025-08-21 | - |
| ADR-0002 | Laufzeit-Framework: Spring Boot | Akzeptiert | 2025-08-21 | - |
| … | … | … | … | … |
```

## Schreibschutz & Bestätigung

* Zeige **Diff** für neue/aktualisierte ADRs und `INDEX.md`.
* Schreibe nur nach Bestätigung.

## Exit-Kriterien

* `export/adr/` enthält ADRs für alle **entscheidenden** Architektur- und Technologiewahlen aus `design/selections.md`.
* Supersede-Beziehungen sind gesetzt, `INDEX.md` ist konsistent.
* Bei `--restart` wurden alte ADRs in `export/adr/<timestamp>/` verschoben und neues Set generiert.


