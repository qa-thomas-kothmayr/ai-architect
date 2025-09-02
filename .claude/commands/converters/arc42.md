---
description: arc42-Architekturdokumentation aus vorhandenen Design-Dokumenten generieren
argument-hint: [--restart]
allowed-tools: Read, Edit, Write
---

## Zweck
Aus den **Design-Dokumenten** (`design/*.md`) und **Context-Informationen** (`context/*.md`) wird eine vollständige, **ausführliche** arc42-Architekturdokumentation generiert. Das Command analysiert vorhandene Strukturen und erstellt alle 12 arc42-Kapitel mit umfangreichen Textbeschreibungen und ergänzenden Mermaid-Diagrammen.

**Fokus auf Content-Tiefe**: Jedes arc42-Kapitel soll substanziellen Textinhalt haben - detaillierte Architekturanalyse mit Business-Kontext, technischen Details, Begründungen und praktischen Beispielen.

## Eingaben
- **Basis-Referenz:** `design/*.md`
- **Context:** `context/*.md`
- **Optional:** `--restart` (sichert alte Version und startet neu)

## Outputs
- **Verzeichnis:** `export/arc42/` mit modularer Struktur
- **Sprache:** Ausschließlich Deutsch (alle Inhalte, Diagramm-Labels, Metadaten)
- **Index:** `export/arc42/INDEX.md` (Übersicht und Navigation)
- **Kapitel:** Separate `.md`-Dateien pro arc42-Kapitel
- **Diagramme:** Separate `.mmd`-Dateien pro Diagramm

## Vorgehen
1) **Backup bei --restart**: Falls `export/arc42/` existiert:
   - Erstelle `export/backup-{timestamp}/arc42/` (komplettes Verzeichnis)
   - Starte komplett neu

2) **Update-Modus**: Ohne `--restart` bei existierendem Verzeichnis:
   - Analysiere bestehende `export/arc42/` Struktur
   - Identifiziere Änderungen in Source-Dokumenten
   - Führe Refinement/Update durch

3) **Content Generation Strategy**:
   - Automatische Inhaltsverzeichnis-Generierung für INDEX.md
   - Hierarchische Überschriftenstruktur (H1 für Kapiteltitel, H2 für Hauptabschnitte, H3 für Details)
   - Navigierbare Querverweise zwischen Kapiteln
   - Konsistente Terminologie und Formatierung durchgängig

4) **Analyse**: Lese alle relevanten Design- und Context-Dokumente:
   - `design/structure.md` → Bausteinsicht und Komponenten identifizieren
   - `design/selections.md` → Lösungsstrategie und Technologieentscheidungen extrahieren  
   - `design/operability.md` → Verteilungssicht und Querschnittliche Konzepte ableiten
   - `context/domain.md` → Kontextabgrenzung und fachliche Anforderungen
   - `context/integrations.md` → Externe Systeme und Schnittstellen

5) **arc42-Mapping**: Transformiere gefundene Strukturen zu arc42-Kapiteln:
   - **Kapitel 1-2**: Ziele und Randbedingungen aus Context
   - **Kapitel 3**: Kontextabgrenzung aus Domain und Integrations
   - **Kapitel 4**: Lösungsstrategie aus Selections
   - **Kapitel 5**: Bausteinsicht aus Structure
   - **Kapitel 6-7**: Laufzeit- und Verteilungssicht aus Operability
   - **Kapitel 8**: Querschnittliche Konzepte aus Design-Patterns
   - **Kapitel 9**: Architekturentscheidungen aus vorhandenen ADRs
   - **Kapitel 10-12**: Qualität, Risiken, Glossar

   **Ausführlichkeitsgrad**: Jedes Kapitel soll umfassendes Textmaterial enthalten:
   - **Detaillierte Beschreibungen**: Jeden Architekturaspekt ausführlich erklären
   - **Begründungen**: Warum-Fragen beantworten, nicht nur Was-Fragen
   - **Praxisbeispiele**: Konkrete Szenarien und Anwendungsfälle
   - **Trade-off-Analysen**: Architekturentscheidungen mit Alternativen begründen
   - **Implementierungsdetails**: Technische Umsetzung und Konfiguration

6) **Content-First Approach**: Erstelle zuerst umfangreichen Textinhalt, dann Diagramme:
   - **Umfassende Textbeschreibungen**: Mindestens 4-6 Absätze pro Hauptkapitel
   - **Strukturierte Gliederung**: Unterkapitel mit jeweils 2-3 Absätzen
   - **Konkrete Beispiele**: Praxisnahe Szenarien und Code-Beispiele
   - **Architektur-Rationale**: Ausführliche Begründung der Designentscheidungen

7) **Diagramm-Generierung**: Nach dem Text erstelle separate `.mmd`-Dateien für relevante Kapitel:
   - **Meaningful Groupings**: Logische Boundary-Gruppierungen mit domänen-spezifischen Farben
   - **Descriptive Relations**: Beschreibende Verben statt generischer Pfeile (z.B. "sendet Event", "validiert")
   - **Component Descriptions**: Detaillierte Annotations und Tooltips für Architekturelemente
   - **Visual Hierarchy**: Angemessene Abstraktionsebenen für optimale Lesbarkeit
   - **Layout Optimization**: Klarer Informationsfluss und reduzierte visuelle Komplexität
   - **NUR** in `.mmd`-Dateien, NIEMALS in Markdown eingebettet
   - Referenziere die `.mmd`-Datei im entsprechenden Kapitel mit Link und Erklärung
   - **WICHTIG**: Verwende nach der Erstellung der `.mmd`-Dateien den `mermaid-expert` Subagent, um die Mermaid-Syntax zu validieren und zu korrigieren

8) **Validierung**: Prüfe auf:
   - Vollständigkeit aller 12 Kapitel
   - Konsistenz zwischen den Kapiteln
   - Referenz-Integrität zu ADRs und anderen Dokumenten

9) **Template Structure Enhancement**:
   - **Template-Validierung**: Prüfe `templates/arc42.md` auf Vollständigkeit vor Verwendung
   - **Beispiel-Content**: Template mit Muster-Inhalten als Leitfaden für Generierung
   - **Validierung-Marker**: Kennzeichnung von Pflicht- vs. optionalen Abschnitten
   - **Cross-Reference-Templates**: Vordefinierte Verknüpfungsstrukturen zwischen Kapiteln
   - **Quality Gates**: Mindest-Wortanzahl und erforderliche Elemente pro Kapitel
   - **Smart Fallbacks**: Nur bei kritischen fehlenden Informationen Interview-Fragen stellen
   - **Completeness Checks**: Markiere unvollständige Abschnitte explizit für spätere Ergänzung

10) **Review**: Zeige Struktur der zu erstellenden/aktualisierenden `export/arc42/` Dateien

11) **Schreiben**: Nach Bestätigung Verzeichnisstruktur erstellen/aktualisieren

## Formatvorgaben
### Verzeichnisstruktur `export/arc42/`
```
export/arc42/
├── INDEX.md                    # Navigation und Übersicht
├── 01-einfuehrung-ziele.md    # Einführung und Ziele
├── 02-randbedingungen.md      # Randbedingungen
├── 03-kontextabgrenzung.md    # Kontextabgrenzung
├── 03-kontextabgrenzung.mmd   # Context-Diagramm
├── 04-loesungsstrategie.md    # Lösungsstrategie
├── 05-bausteinsicht.md        # Bausteinsicht
├── 05-bausteinsicht.mmd       # Baustein-Diagramm
├── 06-laufzeitsicht.md        # Laufzeitsicht
├── 06-laufzeitsicht.mmd       # Laufzeit-Diagramm
├── 07-verteilungssicht.md     # Verteilungssicht
├── 07-verteilungssicht.mmd    # Deployment-Diagramm
├── 08-querschnittlich.md      # Querschnittliche Konzepte
├── 09-entscheidungen.md       # Architekturentscheidungen
├── 10-qualitaet.md           # Qualitätsanforderungen
├── 11-risiken.md             # Risiken und technische Schulden
└── 12-glossar.md             # Glossar
```

## Content Quality Standards
- **Minimum content per section**: 3-5 substantive paragraphs mit technischer Tiefe
- **Developer-friendly language**: Klare "Was", "Warum", "Wie" Erklärungen
- **Practical examples**: Code-Snippets, Konfigurationsbeispiele, konkrete Anwendungsfälle
- **Cross-referencing**: Verweise zu verwandten Kapiteln, ADRs, und externen Dokumenten
- **Visual organization**: Tabellen für Vergleiche, Listen für Strukturen, konsistente Formatierung
- **Terminology consistency**: Einheitliche Begriffe und Definitionen durchgehend verwenden
- **Context provision**: Business-Kontext und Architekturentscheidungen begründen

### INDEX.md Format
- **Metadata**: System, Version, Agent-ID, Timestamp, Source-Dokumente mit Pfaden
- **Navigation**: Links zu allen 12 arc42-Kapiteln und Diagrammen
- **System Übersicht**: Umfassende Systembeschreibung (4-5 Absätze)
- **Architektur-Überblick**: Zentrale Designentscheidungen und Strukturprinzipien
- **Stakeholder & Zielgruppen**: Zielgruppen der Dokumentation
- **Completeness Status**: Explizite Markierung unvollständiger Kapitel (⚠️ INCOMPLETE)
- **Validierungsregeln**: Status der Vollständigkeits- und Konsistenz-Checks

### Content-Struktur pro arc42-Kapitel
Jedes `.md`-Kapitel soll folgende Struktur haben:

1. **Einführung** (1-2 Absätze, PFLICHT): Zweck und Einordnung des Kapitels
2. **Hauptinhalt** (4-8 Absätze je nach Kapitel, PFLICHT):
   - Detaillierte fachliche und technische Beschreibungen (min. 200 Wörter)
   - Konkrete Beispiele und Anwendungsfälle mit Code/Konfiguration
   - Begründungen und Trade-off-Analysen ("warum so, nicht anders")
   - Implementierungsrichtlinien und Best Practices
3. **Cross-References** (PFLICHT): 
   - `→ Siehe auch: [Kapitel X](XX-kapitelname.md)`
   - `→ Bezug zu: [ADR-YYYY](../adr/ADR-YYYY-titel.md)`
   - `→ Implementiert: [Prinzip Z](../principles/project-principles.md#prinzip-z)`

**Quality Gates pro Kapitel**:
- ✅ Mindestens 3 substanzielle Absätze
- ✅ Mindestens 1 konkretes Beispiel oder Code-Snippet
- ✅ Mindestens 2 Cross-References zu anderen Dokumenten
- ✅ Begründung für getroffene Architekturentscheidungen

Füge die Diagramme im Text ein, wenn Du sie erstellt hast. KEINE Diagramme in der INDEX.md!

**Zielgröße**: 3-6 Bildschirmseiten Text pro Hauptkapitel

**WICHTIG**: Mermaid-Diagramme werden NUR in separaten `.mmd`-Dateien gespeichert!

### Diagramm-Referenzierung
Anstatt Mermaid-Code direkt einzubetten, verweise auf externe `.mmd`-Dateien:

```markdown
## Kontextdiagramm

Siehe: [Kontextabgrenzung](03-kontextabgrenzung.mmd)

*Das Diagramm verdeutlicht die Systemgrenzen und zeigt alle relevanten externen Schnittstellen und Akteure.*
```

**Dateistruktur**:
- `03-kontextabgrenzung.md` → enthält nur Text und Diagramm-Verweis
- `03-kontextabgrenzung.mmd` → enthält nur Mermaid-Code

**Konventionen für `.mmd`-Dateien**:
```
graph TD
    subgraph "Frontend Domain" 
        user[User]:::userClass
    end
    subgraph "Core System"
        system[System Name]:::coreClass
    end
    subgraph "Data Domain"
        database[(Database)]:::dataClass
    end
    
    user -->|"authentifiziert via"| system
    system -->|"persistiert in"| database
    system -->|"ruft API auf"| external[External API]:::externalClass
    
    classDef userClass fill:#e1f5fe
    classDef coreClass fill:#f3e5f5  
    classDef dataClass fill:#e8f5e8
    classDef externalClass fill:#fff3e0
```

**Wichtig**: Text hat Priorität - Diagramme ergänzen, ersetzen nicht!

## Standardisierte Backup-Struktur
Bei `--restart` (einheitlich über alle Converter):
```
export/
├── arc42/                           # Aktuelle Version
│   ├── INDEX.md
│   ├── 01-einfuehrung-ziele.md
│   └── ...
└── backup-YYYYMMDD-HHMMSS/         # ISO 8601 Timestamp
    └── arc42/                       # Gesicherte Version
        ├── INDEX.md
        ├── METADATA.md             # Backup-Info: Datum, Grund, Agent-Version
        └── ...
```

## Einheitliche Metadaten-Standards
- **Timestamp-Format**: ISO 8601 (YYYY-MM-DD HH:MM:SS)
- **Agent-Referenz**: Claude Code v{version} + Command-Name
- **Source-Tracking**: Vollständige Pfade zu genutzten Design-Dokumenten
- **Change-Log**: Kurze Beschreibung der Änderungen seit letztem Export
