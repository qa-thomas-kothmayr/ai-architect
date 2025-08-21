# Architektur-Workshop mit Agent-Commands

Dieses Repository stellt ein agentisches Vorgehen bereit, um Softwarearchitektur systematisch und wiederholbar zu entwickeln. Die Commands laufen über CLI (z. B. `claude` CLI) und erzeugen/aktualisieren Markdown-Artefakte im Projekt.

## Generelles Vorgehen

Das Vorgehen folgt fünf logischen Phasen:

1. **Mit welcher Haltung?** → Principles
2. **Zu welchen Zielen?** → Context, Domain, Workload
3. **Wie genau?** → Options, Selections, Structure, Operability
4. **Wie gut?** → ADR, Review
5. **Export** → ADR-Export, arc42, C4

Die Phasen bauen aufeinander auf. Artefakte werden jeweils als Markdown-Dateien im Repo abgelegt und bei Bedarf im Interview-Stil aktualisiert.

## Commands (logische Reihenfolge)

### Phase 1: Haltung klären
- **`principles`** → leitet von `default-principles.md` projektindividuelle `project-principles.md` ab

### Phase 2: Ziele & Kontext erfassen  
- **`context/01_context`** → klärt Stakeholder, Business Goals, Qualitätsziele, Constraints
- **`context/02_domain`** → ermittelt (artefaktbasiert + Interview) Bounded Contexts, Scope, fachliche Regeln
- **`context/03_workload`** → klassifiziert Systemlast (K/M/G/T-Skalen, Events, Daten, Frequenzen)

### Phase 3: Architektur entwickeln
- **`design/01_options`** → erarbeitet 2–3 Architektur-Optionen mit Trade-offs und relativem Aufwand
- **`design/02_selections`** → trifft verbindliche Entscheidungen zu Architektur & Technologien (Matrix + Begründung)
- **`design/03_structure`** → dokumentiert System-/Container-Struktur, Komponenten, Schnittstellen (neutral für C4/arc42)
- **`design/04_operability`** → erfasst Non-Functional Requirements und Betriebsaspekte

### Phase 4: Qualitätssicherung
- **`review`** → prüft Artefakte auf Konsistenz, Vollständigkeit, Prinzipien-Konformität

### Phase 5: Export
- **`export/adr`** → exportiert ADRs aus bestehenden Design-Dokumenten
- **`export/arc42`** → generiert vollständige arc42-Dokumentation aus Design-Artefakten  
- **`export/c4`** → erstellt C4-Diagramme (Context, Container, Components, Deployment)

## Nutzung

### Erster Durchlauf

* Repository auschecken, CLI aufrufen (logische Reihenfolge):

  ```sh
  # Phase 1: Haltung
  claude /project principles
  
  # Phase 2: Kontext
  claude /project context/01_context
  claude /project context/02_domain
  claude /project context/03_workload
  
  # Phase 3: Architektur
  claude /project design/01_options
  claude /project design/02_selections
  claude /project design/03_structure
  claude /project design/04_operability
  
  # Phase 4: Qualitätssicherung
  claude /project adr
  claude /project review
  
  # Phase 5: Export (optional)
  claude /project export/adr
  claude /project export/arc42
  claude /project export/c4
  ```
* Jeder Schritt führt ein Interview, liest bestehende Artefakte und erzeugt/aktualisiert die Ziel-Datei.

### Wiederholte Aufrufe

* Standard: **Refine-Modus** → erlaubt gezielte Ergänzungen/Korrekturen.
* Mit `--restart`: setzt Artefakt neu auf.
* Mit `--input=<pfad>`: lädt Dokumente/Ordner als zusätzliche Quelle.

### Prinzipien

* Der Mensch bleibt im Driver Seat. Agenten stellen Fragen, schlagen vor, erzeugen Artefakte. Committen/Schreiben passiert erst nach Bestätigung.
* Aufwandsschätzungen nur **relativ**, nie absolut in Wochen/Monaten.
* Konsistenz mit Principles wird geprüft; Abweichungen erfordern Waiver.

## Ergebnis

Am Ende liegt eine konsistente Sammlung von Architektur-Artefakten vor (Markdown + optional ADRs), die sich an **arc42** orientieren und eine solide Entscheidungsgrundlage bilden.

