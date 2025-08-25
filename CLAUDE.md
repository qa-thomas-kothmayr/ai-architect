# CLAUDE.md — Repo Policy & Runtime Contract

## Zweck
Zentrale Leitplanken und Konventionen für alle agentischen Commands in diesem Repo. Ziel: reproduzierbare Ergebnisse, konsistenter Stil, minimale Rückfragen, sauberes Diffing.

## Grundhaltung
- **Human-in-the-loop:** Nutzer bleibt Entscheider; Agent schlägt vor, schreibt nur nach Bestätigung.
- **Kein Zero-Shot-Architecting:** Immer Interview/Discovery vor Synthese.
- **On-the-fly Fragen:** Zusätzliche Fragen, wenn Infos fehlen/unklar sind.
- **Schleife bis „verständlich & vollständig“** oder explizitem Abbruch.

## Lesen & Schreiben (immer)
- **Immer lesen:** `principles/project-principles.md`, `context/context.md` (falls vorhanden jeweilige Domain/Workload/Selections/Structure).
- **Diff-first:** Vor jedem Write geplante Änderungen als Diff zeigen.
- **Deterministische Pfade:** Commands schreiben nur ihre je Command definierte Zieldatei.
- **Sprache:** Deutsch in Artefakten, kurze, präzise Bulletpoints.

## Bewertung & Aufwand
- **Ampelskala:** 🟢 gut/hoch, 🟡 mittel, 🔴 schlecht/niedrig.
- **Aufwand nur relativ** (🟢/🟡/🔴). **Keine** Wochen/Monate.
- **Lock-in, Team-Fit, TCO** immer explizit benennen, falls relevant.

## Prinzipien-Alignment
- Widersprüche zu `project-principles.md` markieren (⚠️) und **Waiver** verlangen (Owner, Ablaufdatum, Begründung).

## Command-Ausführungsreihenfolge
Die Commands folgen 5 logischen Phasen, die aufeinander aufbauen:

### Phase 1: Haltung (Principles)
- **`principles`** → Basis für alle weiteren Entscheidungen

### Phase 2: Ziele & Kontext
- **`domain/01_context`** → Stakeholder, Goals, Constraints, **Team-Kapazitäten**
- **`domain/02_domain`** → Bounded Contexts, Scope  
- **`domain/03_workload`** → Systemlast (K/M/G/T)

### Phase 3: Architektur entwickeln
- **`design/01_options`** → 2 konservative + 1-3 kreative Optionen
- **`design/02_selections`** → Verbindliche Entscheidungen
- **`design/03_structure`** → System-/Container-Struktur
- **`design/04_operability`** → NFRs und Betrieb

### Phase 4: Qualitätssicherung
- **`review`** → Konsistenz-Check aller Artefakte
- **`validate-mermaid`** → Syntax-Validierung aller Diagramme

### Phase 5: Export
- **`converters/adr`** → ADR-Export
- **`converters/arc42`** → arc42-Dokumentation
- **`converters/c4`** → C4-Diagramme

**Wichtig**: Commands der späteren Phasen lesen automatisch Artefakte der früheren Phasen.

## Command-Kontrakt (für alle Commands)
- **Inputs:** optional `--input=<pfad>` (Datei/Ordner) als Initialgrundlage.
- **Refine-Default:** erneuter Aufruf = Klärungen/Updates. `--restart` = von vorne, vorhandene Inhalte überschreiben.
- **Interviewstil:** konkrete, kurze Fragen; Nur notwendige Ja/Nein + Freitext.
- **Outputs:** exakt eine Zieldatei gemäß Command-Spec; keine stillen Nebeneffekte.

## Discovery-Heuristiken (Domain/Structure)
### Artefakt-Scanning
- **API-Definitionen**: `*.yaml`, `*.yml` (OpenAPI/Swagger), `*.proto` (gRPC), `*.graphql`
- **Datenbank-Schema**: `*.sql`, `migrations/*.sql`, `schema.prisma`, `*.dbml`
- **Package-Files**: `package.json`, `pom.xml`, `build.gradle`, `requirements.txt`, `go.mod`, `Cargo.toml`
- **Config-Files**: `docker-compose.yml`, `k8s/*.yaml`, `.env*`, `appsettings.json`
- **Event-Definitionen**: Kafka Topics, RabbitMQ Exchanges, AWS SNS/SQS Configs

### Tech-Stack-Erkennung
- **Sprachen**: Aus File-Extensions (`.java`, `.py`, `.ts`, `.go`, `.cs`, `.rs`)
- **Frameworks**: Aus Dependencies in Package-Files
- **Datenbanken**: Aus Connection-Strings, Docker-Images, Schema-Files
- **Cloud-Services**: Aus Terraform/CloudFormation/ARM Templates
- **CI/CD**: Aus `.github/workflows`, `.gitlab-ci.yml`, `Jenkinsfile`

### Context-Boundary-Indikatoren
- APIs/Schema/Topics → Capabilities/Entities/Events ableiten
- Ownership, Kopplung, Änderungsrate → Schnittkandidaten
- Compliance/PII & Latenzprofile → mögliche Grenzen
- **Neue Indikatoren**:
  - Separate Repos/Module → potenzielle Service-Grenzen
  - Unterschiedliche Tech-Stacks → natürliche Boundaries
  - Team-Zuordnungen in CODEOWNERS → Ownership-Grenzen
  - Deployment-Units → Runtime-Boundaries

## Mermaid-Validierung
### Validierungs-Workflow
- **Command:** `validate-mermaid` nutzt den mermaid-expert Subagent
- **Scope:** Alle `*.mmd` Dateien im Projekt
- **Zeitpunkt:** Nach Diagramm-Erstellung, vor Export-Phase

### Häufige Syntax-Fehler
- **Fehlende Quotes** bei Knoten-Labels mit Sonderzeichen
- **Ungültige Pfeil-Syntax** (z.B. `-->` statt `->` in State-Diagrams)
- **Fehlende Semikolons** am Zeilenende (in manchen Diagram-Typen)
- **Inkonsistente Knoten-IDs** (Definition vs. Referenz)
- **Ungültige Subgraph-Verschachtelung**

### Diagramm-Komplexitätslimits
- **Max. Knoten pro Diagramm:** ~50 (darüber unleserlich)
- **Max. Verschachtelungstiefe:** 3 Ebenen
- **Max. Verbindungen pro Knoten:** 7 (sonst Spaghetti)
- Bei Überschreitung → Aufteilen in mehrere Diagramme

### Validierungs-Output
- **Erfolg:** Grüne Bestätigung pro Datei
- **Fehler:** Datei, Zeile, Fehlerbeschreibung
- **Warnung:** Komplexitäts-Hinweise, Style-Vorschläge

## Konsistenz-Checks (vor Write)
- **Context-Fit:** Ziele/Constraints spiegeln.
- **Workload-Fit:** K/M/G/T, RPH/Tag ↔ Struktur/Operability.
- **Options↔Selections:** Trade-offs/Abwägungen konsistent.
- **Mermaid-Lint:** Diagramme syntaktisch geprüft (falls erzeugt).

## Reviews
- Schweregrade: 🟥 High / 🟧 Medium / 🟨 Low.
- Findings immer mit **Quelle/Beleg** (Datei+Abschnitt) und **konkretem Vorschlag**.

## ADRs
- Ablage: `export/architecture-decision-records/`.
- Nummern fortlaufend; Supersede-Beziehungen pflegen; `INDEX.md` aktualisieren.
- Quellen verlinken (Selections/Options/Operability/Principles).

## Fehler & Unklarheiten
- **Keine Halluzinationen:** Unbekanntes als Frage kennzeichnen.
- **Konflikte:** Explizit auflisten, Entscheidung vertagen oder Waiver vorschlagen.

## Erweiterung
- Neue Commands müssen diese Datei respektieren.

