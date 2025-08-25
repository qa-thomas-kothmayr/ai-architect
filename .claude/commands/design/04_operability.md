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
2) **Interview (schrittweise, eine Kategorie und Frage pro Schritt):**
   
   **Verfügbarkeit:**
   - "Welche Verfügbarkeit erwarten Sie für das System?" (Beispiele zeigen: 99,5% / 99,9% / 99,99%)
   - Bei Bedarf Nachfrage: "Sind geplante Wartungsfenster akzeptabel?"
   
   **Latenz/Performance:**
   - "Welche Antwortzeiten erwarten Sie?" (Antwort abwarten)
   - "Welchen Durchsatz muss das System schaffen?" (Antwort abwarten)  
   - "Gibt es spezielle SLA-Anforderungen?" (Antwort abwarten)
   
   **Skalierbarkeit:**
   - "Wie soll das System skalieren - horizontal oder vertikal?" (Antwort abwarten)
   - "In welcher Workload-Klasse bewegen wir uns?" (K/M/G/T-Klassen erklären)
   
   **Zuverlässigkeit & Resilienz:**
   - "Brauchen Sie automatisches Failover?" (Antwort abwarten)
   - "Ist Redundanz erforderlich?" (Antwort abwarten)
   - "Soll das System self-healing sein?" (Antwort abwarten)
   
   **Observability:**
   - "Welche Art von Monitoring brauchen Sie?" (Antwort abwarten)
   - "Sind structured Logs wichtig?" (Antwort abwarten)
   - "Brauchen Sie distributed Tracing?" (Antwort abwarten)
   
   **Security & Privacy:**
   - "Welche Authentifizierung/Autorisierung ist erforderlich?" (Antwort abwarten)
   - "Brauchen Sie Verschlüsselung?" (Antwort abwarten)
   - "Gibt es DSGVO- oder Compliance-Anforderungen?" (Antwort abwarten)
   
   **Operabilität:**
   - "Wie soll das Deployment funktionieren?" (Antwort abwarten)
   - "Wie wichtig ist einfache Konfigurierbarkeit?" (Antwort abwarten)
   - "Brauchen Sie Backup/Restore-Strategien?" (Antwort abwarten)
   - "Ist Disaster Recovery relevant?" (Antwort abwarten)
   
   **Wartbarkeit & Evolvierbarkeit:**
   - "Wie häufig planen Sie Upgrades?" (Antwort abwarten)
   - "Ist Abwärtskompatibilität wichtig?" (Antwort abwarten)
   
   **Kostenrahmen:**
   - "Haben Sie grobe Kostenvorstellungen?" (nur relative Angaben erwarten: niedrig/mittel/hoch)
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

