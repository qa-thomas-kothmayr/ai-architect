# ADR-<NNNN>: <Titel>

## Status
Vorgeschlagen | Akzeptiert | Abgelehnt | Überholt | Veraltet | {Datum}

## Metadaten (PFLICHT)
- Entscheidungs-Owner: <Team/Person>
- Reviewers: <Liste>
- Gültig ab: {Datum}
- Agent-Version: Claude Code v{version} + adr
- Source-Dokumente: [design/selections.md](../design/selections.md), [principles/project-principles.md](../principles/project-principles.md)

## Verwandte ADRs
- Ersetzt: ADR-YYYY: <Titel> (falls zutreffend)
- Ersetzt durch: ADR-YYYY: <Titel> (bei Ablösung in Zukunft)
- Siehe auch: ADR-YYYY: <Titel>

## Kontext (PFLICHT, min. 100 Wörter)
**Geschäfts- und technischer Hintergrund:** 
Kurzfassung relevanter Ziele/Constraints (aus `context/context.md`), Prinzipien, Workload-Fakten.

**Beispiel-Inhalt:** Das E-Commerce-System benötigt eine hochperformante OLTP-Datenbank für Katalogdaten und Bestellabwicklung. Workload: 10K RPH, <100ms Latenz erforderlich...

## Entscheidung (PFLICHT, min. 150 Wörter) 
**Was wird entschieden:** Die Entscheidung knapp und aktiv formuliert.
**Beispiel:** „Wir wählen PostgreSQL als primäre OLTP-Datenbank für Produktkatalog und Bestellsystem."

**Detaillierte Umsetzung:** Konkrete Implementierungsschritte, Konfigurationshinweise, betroffene Services.

## Begründung (PFLICHT)
**Warum diese Entscheidung?** 
- Bezug auf Prinzipien & Geschäftsziele (min. 2 Referenzen)
- **Ampel-Bewertung:** 🟢/🟡/🔴 für Zielerreichung, Evolvierbarkeit, Operabilität, Security/Privacy, Kosten (TCO), Aufwand (relativ), Team-Fit, Lock-in

**Betrachtete Alternativen (mind. 3):**
1. Alternative A: Warum abgelehnt
2. Alternative B: Warum abgelehnt  
3. Alternative C: Warum abgelehnt

## Konsequenzen (PFLICHT)
**Positive Auswirkungen (mind. 2):**
- Konkrete Vorteile, messbare Verbesserungen

**Negative Auswirkungen/Risiken (mind. 2):**
- Identifizierte Risiken, Mitigation-Maßnahmen

**Folgeaufgaben:**
- Konkrete nächste Schritte, Verantwortlichkeiten

## Cross-References (PFLICHT, mind. 1)
- **→ Implementiert Prinzip:** [Prinzip X](../principles/project-principles.md#prinzip-x)
- **→ Bezug zu Selections:** [Design Selections](../design/selections.md#abschnitt)
- **→ Verwandte ADRs:** [ADR-XXXX](ADR-XXXX-titel.md)
- **→ Options-Analyse:** [Design Options](../design/options.md#abschnitt)
- **→ Operability-Impact:** [Operability](../design/operability.md#abschnitt)

## Temporäre Abweichungen
- Beschreibung: <Wovon wird abgewichen?>
- Begründung: <Warum notwendig?>
- Ablaufdatum / Review-Datum: YYYY-MM-DD
- Verantwortlich: <Name/Rolle>

## Compliance / Zuordnung
- <Standard / Norm>: Prinzip/Aspekt
- …

