# Default Architecture Principles

## P01 – Langweilige Software ist gute Software
- **Leitlinie**: Bevorzugt Technologien und Patterns, die bewährt, robust und gut verstehbar sind.
- **Rationale**: Vorhersagbare Software ist leichter zu betreiben, zu warten und zu debuggen.
- **Konsequenzen**: Kein unnötiger Hype. Innovation nur, wenn sie echten Produktivitäts- oder Geschäftsnutzen bringt.
- **Beispiel**: Lieber etablierte DB wie Postgres als ein unreifes neues DB-Produkt.
- **Tags**: simplicity, predictability

## P02 – Gut betreibbar von Anfang an
- **Leitlinie**: Systeme werden so gebaut, dass Betriebsteams sie problemlos handhaben können.
- **Rationale**: Wir selbst machen kein Ops, aber unsere Software muss für andere klar, stabil und supportbar sein.
- **Konsequenzen**: Logging, Monitoring-Hooks, saubere Schnittstellen, Failover-Strategien sind Pflicht.
- **Tags**: operability, devops

## P03 – Sicherheit & Datenschutz by Design
- **Leitlinie**: Security und Privacy sind integraler Bestandteil, keine Add-ons.
- **Rationale**: Vertrauen und Compliance sind Grundpfeiler jeder nachhaltigen Lösung.
- **Konsequenzen**: Bedrohungsmodellierung, Privacy Default, Secret Management von Anfang an.
- **Tags**: security, privacy

## P04 – Evolvierbarkeit über Optimierung
- **Leitlinie**: Wir entwerfen so, dass Änderungen und Erweiterungen einfach möglich sind – Optimierung kommt nach Messung.
- **Rationale**: Anforderungen ändern sich schneller als Hardware; starre Optimierungen kosten später viel.
- **Konsequenzen**: Klare Modularisierung, Schema-Evolution, refactoringfreundlicher Code.
- **Tags**: evolvability, flexibility

## P05 – Qualitätseigenschaften als Leitplanken
- **Leitlinie**: Performance, Skalierbarkeit, Sicherheit, Wartbarkeit und Kostenbewusstsein steuern Architekturentscheidungen.
- **Rationale**: Nicht-funktionale Eigenschaften entscheiden über Akzeptanz und Lebensdauer.
- **Konsequenzen**: Szenario-getriebene Reviews, explizite Trade-offs.
- **Tags**: quality, nfr

## P06 – Dokumentierte Entscheidungen
- **Leitlinie**: Architekturentscheidungen sind transparent, nachvollziehbar und versioniert.
- **Rationale**: Nur dokumentierte Entscheidungen sind überprüfbar und tragfähig.
- **Konsequenzen**: ADRs sind Standard. Abweichungen brauchen Waiver mit Ablaufdatum.
- **Tags**: adr, transparency

## P07 – Cloud Native & Open Source, mit Augenmaß
- **Leitlinie**: Offene Standards und Cloud-native Services werden bevorzugt, aber nur wo sie Mehrwert bringen.
- **Rationale**: Reduziert Lock-in, erhöht Produktivität. Aber Hype-Services ohne Reifegrad meiden.
- **Konsequenzen**: Tech-Entscheidungen müssen Nutzen, Risiken und Kosten abwägen.
- **Tags**: cloud, open-source

## P08 – Am Puls der Zeit, aber produktiv
- **Leitlinie**: Technologien werden eingeführt, wenn sie reif genug sind und Produktivität oder Qualität signifikant erhöhen.
- **Rationale**: Zu spät sein kostet Anschluss, zu früh sein kostet Stabilität.
- **Konsequenzen**: Neue Tools erst nach Spike und Business-Case einführen.
- **Tags**: innovation, pragmatism

## P09 – Bedarfspassgenau, nicht overengineered
- **Leitlinie**: Lösungen so einfach wie möglich, aber nicht einfacher – zugeschnitten auf den Bedarf und die absehbare Entwicklung des Kunden.
- **Rationale**: Hyperscale-Architekturen oder Technikspielereien führen zu Kosten und Risiken ohne Nutzen.
- **Konsequenzen**: Skalierung nur im realistischen Maß. Keine „Architektur auf Vorrat“.
- **Tags**: fit-for-purpose, simplicity

