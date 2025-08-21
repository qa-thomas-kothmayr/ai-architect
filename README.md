# Architektur-Workshop mit Agent-Commands

Dieses Repository stellt ein agentisches Vorgehen bereit, um Softwarearchitektur systematisch und wiederholbar zu entwickeln. Die Commands laufen über CLI (z. B. `claude` CLI) und erzeugen/aktualisieren Markdown-Artefakte im Projekt.

## Generelles Vorgehen

Das Vorgehen folgt vier Gruppen von Fragen:

1. **Mit welcher Haltung?** → Principles
2. **Zu welchen Zielen?** → Context, Domain, Workload
3. **Wie genau?** → Options, Selections
4. **Wie gut?** → Review

Die Phasen bauen aufeinander auf. Artefakte werden jeweils als Markdown-Dateien im Repo abgelegt und bei Bedarf im Interview-Stil aktualisiert.

## Commands

Alle Commands liegen unter `.claude/commands/…` und sind im CLI verfügbar:

* `principles` → leitet von `default-principles.md` projektindividuelle `project-principles.md` ab.
* `context` → klärt Rahmenbedingungen, Inputs und Zielsetzungen.
* `domain` → ermittelt (artefaktbasiert + Interview) die fachliche Domäne, Regeln, Policies.
* `workload` → klassifiziert Systemlast (K/M/G/T, Events, Daten, Frequenzen).
* `options` → erarbeitet 2–3 Architektur-Optionen mit Trade-offs und Aufwand.
* `selections` → trifft verbindliche Entscheidungen zu Architektur-Optionen und Technologien, dokumentiert Matrix und Begründung.
* `review` → prüft ausgewählte Artefakte oder ganze Gruppen auf Konsistenz und Vollständigkeit.

## Nutzung

### Erster Durchlauf

* Repository auschecken, CLI aufrufen:

  ```sh
  claude /project principles
  claude /project context
  claude /project domain
  claude /project workload
  claude /project options
  claude /project selections
  ```
* Jeder Schritt führt ein Interview, liest bestehende Artefakte und erzeugt/aktualisiert die Ziel-Datei.

### Wiederholte Aufrufe

* Standard: **Refine-Modus** → erlaubt gezielte Ergänzungen/Korrekturen.
* Mit `--restart`: setzt Artefakt neu auf.
* Mit `--input=<pfad>`: lädt Dokumente/Ordner als zusätzliche Quelle.
* Mit `--export=adr`: erzeugt ADR-Drafts (Entscheidungsprotokolle).

### Prinzipien

* Der Mensch bleibt im Driver Seat. Agenten stellen Fragen, schlagen vor, erzeugen Artefakte. Committen/Schreiben passiert erst nach Bestätigung.
* Aufwandsschätzungen nur **relativ**, nie absolut in Wochen/Monaten.
* Konsistenz mit Principles wird geprüft; Abweichungen erfordern Waiver.

## Ergebnis

Am Ende liegt eine konsistente Sammlung von Architektur-Artefakten vor (Markdown + optional ADRs), die sich an **arc42** orientieren und eine solide Entscheidungsgrundlage bilden.

