---
description: Operabilität & Non-Functional Requirements (NFRs) erfassen und dokumentieren
argument-hint: [--input=pfad/zum/ordner-oder-dokument] [--restart]
allowed-tools: Read, Edit
---

## Zweck
Sammelt und dokumentiert **Qualitätsanforderungen** sowie Aspekte der **Betriebsfähigkeit** des Systems. Ziel ist ein Artefakt `design/operability.md`, das beschreibt, wie gut das System im Betrieb funktionieren muss (z. B. Verfügbarkeit, Observability, Sicherheit, Compliance).

## Eingaben (read-only)
- `principles/project-principles.md` (immer gelesen)
- `context/context.md`, `context/domain.md`, `context/workload.md` (immer gelesen, falls vorhanden)
- `design/*.md` (immer gelesen, um Abhängigkeiten zu bewerten)
- `--input`: Ordner/Dokumente (z. B. Sicherheitsanforderungen, Betriebsrichtlinien)

## Outputs
- **Immer:** `design/operability.md` mit priorisierten NFRs & Betriebsanforderungen

## Aufruf-Logik
- **Erster Aufruf:** Interview führt durch Kategorien, erfasst Anforderungen & Erwartungen.
- **Erneuter Aufruf:** Refine-Modus → Ergänzungen, Präzisierungen, Änderungen.
- **Mit `--restart`:** setzt Dokument neu auf.

## Vorgehen
1) **Lesen & Prüfen**
   - Principles, Context, Workload & Selections laden.
2) **Interview** (Fragen je Kategorie; on-the-fly Zusatzfragen erlaubt):
   - **Verfügbarkeit** (z. B. 99,5% / 99,9% / 99,99%)
   - **Latenz/Performance** (Antwortzeiten, Durchsatz, SLAs)
   - **Skalierbarkeit** (Skalierungsstrategie, K/M/G/T-Klassen)
   - **Zuverlässigkeit & Resilienz** (Failover, Redundanz, Self-Healing)
   - **Observability** (Monitoring, Logging, Tracing)
   - **Security & Privacy** (AuthN/Z, Verschlüsselung, DSGVO, Compliance)
   - **Operabilität** (Deployment, Konfigurierbarkeit, Backup/Restore, Disaster Recovery)
   - **Wartbarkeit & Evolvierbarkeit** (Upgrade-Zyklen, Abwärtskompatibilität)
   - **Kostenrahmen** (grobe Erwartungen, nur relativ)
3) **Artefakt erzeugen**
   - Ampelbewertung (🟢/🟡/🔴) oder Ja/Nein, wo sinnvoll.
   - Priorisierung (MUST / SHOULD / NICE-TO-HAVE).
   - Ergänzende Texte (Begründungen, Constraints, offene Fragen).
4) **Diff zeigen → Schreiben**
   - Änderungen an `design/operability.md` erst nach Bestätigung schreiben.

## Formatvorgaben
### `design/operability.md`
```md
# Operability & Non-Functional Requirements

## Availability
- Ziel: 99,9% (MUST)
- Bemerkungen: Betrieb in 2 AZs, automatisches Failover 🟢

## Latency & Performance
- Antwortzeiten: < 200ms für 95% aller Requests (SHOULD)
- Durchsatz: bis zu 10k req/min 🟡

## Scalability
- Horizontale Skalierung Services 🟢
- DB-Partitionierung vorbereitet 🔴

## Reliability & Resilience
- Automatisches Restart bei Crash (MUST)
- Chaos Testing geplant (NICE-TO-HAVE)

## Observability
- Structured Logging (MUST)
- Distributed Tracing (SHOULD)
- Metriken (Prometheus/Grafana) 🟢

## Security & Privacy
- AuthN/Z via OIDC (MUST)
- Data-at-rest Encryption (MUST)
- DSGVO-konforme Löschkonzepte (SHOULD)

## Operability
- Deployment: automatisiert (CI/CD) 🟢
- Config via Env Vars (12-Factor) 🟢
- Backup & Restore wöchentlich getestet (MUST)

## Maintainability
- Major Upgrades: halbjährlich geplant (SHOULD)
- API-Kompatibilität: min. 2 Versionen parallel (MUST)

## Cost Expectations
- Cloud-Kostenrahmen: mittel 🟡

## Open Questions
- SLA mit Kunde noch offen
- Recovery Time Objective (RTO) noch zu klären
```

## Validierung

* **Konsistenz:** Anforderungen widersprechen nicht Principles/Selections.
* **Vollständigkeit:** Jede Hauptkategorie adressiert oder explizit „nicht relevant“.
* **Priorisierung:** Muss-Kriterien klar markiert.

## Exit-Kriterien

* `design/operability.md` existiert mit NFRs in allen Kernkategorien.
* Ampel-/MUST-SHOULD-Markierungen enthalten.

