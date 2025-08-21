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
- **Sprache:** Deutsch, wenn nicht vom Nutzer anders gefordert
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

3) **Analyse**: Lese alle relevanten Design- und Context-Dokumente:
   - `design/structure.md` → Bausteinsicht und Komponenten identifizieren
   - `design/selections.md` → Lösungsstrategie und Technologieentscheidungen extrahieren  
   - `design/operability.md` → Verteilungssicht und Querschnittliche Konzepte ableiten
   - `context/domain.md` → Kontextabgrenzung und fachliche Anforderungen
   - `context/integrations.md` → Externe Systeme und Schnittstellen

4) **arc42-Mapping**: Transformiere gefundene Strukturen zu arc42-Kapiteln:
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

5) **Content-First Approach**: Erstelle zuerst umfangreichen Textinhalt, dann Diagramme:
   - **Umfassende Textbeschreibungen**: Mindestens 4-6 Absätze pro Hauptkapitel
   - **Strukturierte Gliederung**: Unterkapitel mit jeweils 2-3 Absätzen
   - **Konkrete Beispiele**: Praxisnahe Szenarien und Code-Beispiele
   - **Architektur-Rationale**: Ausführliche Begründung der Designentscheidungen

6) **Diagramm-Generierung**: Nach dem Text erstelle separate `.mmd`-Dateien für relevante Kapitel:
   - Verwende camelCase-Namenskonventionen
   - Medium Abstraktionslevel
   - Konsistente Farb- und Symbol-Kodierung
   - **NUR** in `.mmd`-Dateien, NIEMALS in Markdown eingebettet
   - Referenziere die `.mmd`-Datei im entsprechenden Kapitel mit Link und Erklärung
   - **WICHTIG**: Verwende nach der Erstellung der `.mmd`-Dateien den `mermaid-expert` Subagent, um die Mermaid-Syntax zu validieren und zu korrigieren

7) **Validierung**: Prüfe auf:
   - Vollständigkeit aller 12 Kapitel
   - Konsistenz zwischen den Kapiteln
   - Referenz-Integrität zu ADRs und anderen Dokumenten

8) **Template-Anwendung**: Nutze `templates/arc42.md` als Strukturbasis

9) **Review**: Zeige Struktur der zu erstellenden/aktualisierenden `export/arc42/` Dateien

10) **Schreiben**: Nach Bestätigung Verzeichnisstruktur erstellen/aktualisieren

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

### INDEX.md Format
- **Metadata**: System, Version, Agent-ID, Timestamp
- **Navigation**: Links zu allen 12 arc42-Kapiteln und Diagrammen
- **System Übersicht**: Umfassende Systembeschreibung (4-5 Absätze)
- **Architektur-Überblick**: Zentrale Designentscheidungen und Strukturprinzipien
- **Stakeholder & Zielgruppen**: Zielgruppen der Dokumentation
- **Validierungsregeln**: Status der Vollständigkeits- und Konsistenz-Checks

### Content-Struktur pro arc42-Kapitel
Jedes `.md`-Kapitel soll folgende Tiefe haben:

1. **Einführung** (1-2 Absätze): Zweck und Einordnung des Kapitels
2. **Hauptinhalt** (4-8 Absätze je nach Kapitel):
   - Detaillierte fachliche und technische Beschreibungen
   - Konkrete Beispiele und Anwendungsfälle
   - Begründungen und Trade-off-Analysen
   - Implementierungsrichtlinien und Best Practices
3. **Referenzen**: Verknüpfungen zu ADRs und anderen Dokumenten

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
    user[User] --> system[System Name]
    system --> database[(Database)]
    system --> external[External API]
```

**Wichtig**: Text hat Priorität - Diagramme ergänzen, ersetzen nicht!

## Backup-Struktur
Bei `--restart`:
```
export/
├── arc42/                      # Neue modulare Version
│   ├── INDEX.md
│   ├── 01-einfuehrung-ziele.md
│   └── ...
└── backup-20240821-143022/     # Timestamp-Ordner
    └── arc42/                  # Gesichertes Verzeichnis
        ├── INDEX.md
        └── ...
```
