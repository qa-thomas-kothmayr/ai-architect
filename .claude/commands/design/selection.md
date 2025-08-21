---
description: Architektur- und Technologieauswahl konsolidieren und verbindlich festhalten
argument-hint: [--input=pfad/zum/ordner-oder-dokument] [--restart] [--export=adr]
allowed-tools: Read, Edit
---

## Zweck
Konsolidiert **Architektur-Optionen** und **Technologieauswahl** zu einer verbindlichen Entscheidung. Liest **immer** `design/options.md`, `principles/project-principles.md` sowie `context/context.md`/`context/domain.md`/`context/workload.md` (falls vorhanden). Arbeitet im Interview-Stil und dokumentiert das Ergebnis in `design/selections.md`. **Keine absoluten Zeitangaben**, Aufwand nur **relativ** (🟢/🟡/🔴).

## Eingaben (read-only)
- `design/options.md` (immer gelesen)
- `principles/project-principles.md` (immer gelesen)
- `context/*.md` (immer gelesen, falls vorhanden)
- `--input`: Ordner/Dokumente als zusätzliche Quellen (z. B. RFCs, Spike-Ergebnisse)

## Outputs
- **Immer:** `design/selections.md` (gewählte Option(en) + Tech-Stack + Begründung)
- **Optional:** bei `--export=adr` → ADRs für Kernentscheidungen unter `design/adrs/ADR-xxxx-<topic>.md`
- **Zusätzlich:** automatisch "Rejected Alternatives" Abschnitt (aus `design/options.md` übernommen)

## Aufruf-Logik
- **Erster Aufruf:** fragt zuerst, ob eine Option (oder Kombination) bereits favorisiert ist; führt dann Tech-Bewertung durch.
- **Erneuter Aufruf:** **Refine-Modus** – gezielte Klärungen/Updates zu bereits getroffenen Entscheidungen.
- **Mit `--restart`:** ignoriert bestehende Inhalte und startet neu.

## Vorgehen
1) **Lesen & Prüfen**
   - Ziele/Constraints/Workload/Principles laden.
   - Optionen aus `design/options.md` einlesen.
   - **Prinzipien-Check**: markiere Konflikte (⚠️) und verlange Waiver, falls Entscheidung dagegen läuft.

2) **Optionsauswahl (Interview)**
   - Frage: "Gibt es eine klare Favoriten-Option oder eine Kombination?" → Nutzerantwort übernehmen.
   - Falls unklar: Kurzdarstellung der Optionen mit Ampelbewertung aus `design/options.md` und gezielten Rückfragen.
   - Ergebnis: **gewählte Option(en)** + kurze Begründung; **verworfen**: Gründe knapp notieren.

3) **Technologieauswahl (Matrix)**
   - Kategorien vorschlagen die zu den Optionen und dem Kontext passen. Beispiele, die aber nicht immer abgefragt werden müssen: **Runtime/Framework**, **Datenhaltung**, **Messaging/Integration**, **API/Edge**, **Infra/Orchestration**, **Observability**, **Security**, **CI/CD**.
   - Für jede Kategorie **2–4 Kandidaten** gegenüberstellen.
   - Bewertung je Kriterium mit Ampel (🟢 gut/hoch, 🟡 mittel, 🔴 schlecht/niedrig). **Keine Zahlen-/Gewichtsspielchen.**
   - Kriterien (erweiterbar): **Zielerreichung**, **Evolvierbarkeit**, **Time-to-Market**, **Operabilität**, **Security/Privacy-Fit**, **Kosten (TCO grob)**, **Entwicklungsaufwand (relativ)**, **Team-Fit**, **Lock-in**.
   - Der Agent darf **on the fly** Zusatzfragen stellen (z. B. Team-Erfahrung, Compliance-Forderungen, Hosting-Vorgaben).

4) **Konsolidierung & Entscheidung**
   - **Entscheidungspaket** erzeugen: gewählte Option(en) + je Kategorie der gewählte Technologie-Kandidat.
   - **Begründung** pro Wahl (1–3 Sätze) + **Risiken & Mitigation** (Stichpunkte).
   - **Waiver** erzeugen, wenn Prinzipienkonflikt bewusst akzeptiert wird (mit Ablaufdatum/Owner).

5) **Diff zeigen → Schreiben**
   - Änderungen an `design/selections.md` nur nach Bestätigung schreiben. Bei `--export=adr`: ADRs generieren.

## Formatvorgaben
### `design/selections.md`
```md
# Architecture & Technology Selections

## Summary
- Gewählte Option(en): …
- Kerngründe: …
- Haupt-Risiken & Mitigations: …

## Selected Architecture
- Option(en): … (Kurzbegründung)
- Abhängigkeiten/Impakts: …

## Technology Matrix (Ampelbewertung)
### Kategorie: <z. B. Datenhaltung>
| Kriterium | Postgres | DynamoDB | … |
|---|:---:|:---:|:---:|
| Zielerreichung | 🟢 | 🟢 | … |
| Evolvierbarkeit | 🟢 | 🟡 | … |
| Time-to-Market | 🟢 | 🟡 | … |
| Operabilität | 🟢 | 🟢 | … |
| Security/Privacy | 🟡 | 🟢 | … |
| Kosten (TCO) | 🟢 | 🟡 | … |
| Aufwand (relativ) | 🟢 | 🟡 | … |
| Team-Fit | 🟢 | 🟡 | … |
| Lock-in | 🟢 | 🔴 | … |

### Kategorie: <z. B. Runtime/Framework>
| Kriterium | Spring Boot | Node/NestJS | … |
|---|:---:|:---:|:---:|
| Zielerreichung | 🟢 | 🟡 | … |
| Evolvierbarkeit | 🟢 | 🟡 | … |
| Time-to-Market | 🟢 | 🟢 | … |
| Operabilität | 🟢 | 🟡 | … |
| Security/Privacy | 🟡 | 🟡 | … |
| Kosten (TCO) | 🟡 | 🟢 | … |
| Aufwand (relativ) | 🟡 | 🟡 | … |
| Team-Fit | 🟢 | 🟢 | … |
| Lock-in | 🟡 | 🟡 | … |

## Decision & Rationale
- Architektur-Entscheidung: … (Warum diese, warum nicht die anderen)
- Technologie-Entscheidungen je Kategorie: …
- Prinzipienkonflikte & Waiver: …

## Rejected Alternatives
- Option B: … (kurz)
- Kandidat X (Kategorie Y): … (kurz)

## Folgen & nächste Schritte
- Spikes/Proofs zur Risikoreduktion: …
- Migrations-/Einführungsplan (nur grob, relativ): …
