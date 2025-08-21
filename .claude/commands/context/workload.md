---
description: Projekt-Workload erfassen (K/M/G/T/0, J/N Antworten)
argument-hint: [--export=adr]
allowed-tools: Read, Edit
---

## Zweck
Erfasst **Mengengerüste, Lastprofile und Wachstum** im Interview-Stil. Antworten sind **K/M/G/T/0** (Größenordnung) oder **J/N** (mit Folgefrage bei J). Ergebnisse landen konsistent in `context/workload.md`; optional wird ein ADR erzeugt.

## Skalen & Einheiten
- **K = ~10³**, **M = ~10⁶**, **G = ~10⁹**, **T = ~10¹²**, **0 = nicht zutreffend**
- **Requests**: Requests pro Stunde (**RPH**)
- **Events**: Events pro **Tag**
- **Nutzer**: absolute Anzahl
- **Daten**: Records oder Volumen (GB/TB) – je Frage angegeben

## Outputs
- **Immer:** `context/workload.md` (strukturierter Bericht inkl. Klassifikation & Annahmen)
- **Optional:** `design/adrs/ADR-????-workload.md` (wenn `--export=adr`), checke die nächsthöhere Nummer

## Interview-Loop
Führe die folgenden Blöcke **sequenziell** aus. **Bleibe im Frage-Antwort-Zyklus**, bis alle relevanten Aspekte beantwortet sind oder der Nutzer explizit abbricht.

### 1) Nutzer & Concurrency
Fragen (Antwort: K/M/G/T/0, sonst wie angegeben):
- Gleichzeitige Nutzer (Concurrency): [K/M/G/T/0]
- Gesamtnutzer / Accounts: [K/M/G/T/0]
- Mehrfachgeräte pro Nutzer relevant? [J/N] → bei J: "Wie viele typischerweise? (Ø/Max)"

Checks:
- p95-Heuristik: Wenn Concurrency = M/G/T → später **Skalierungs- und Caching-Strategie** anmahnen.

### 2) Requests pro Stunde (RPH)
- Reads RPH: [K/M/G/T/0]
- Writes RPH: [K/M/G/T/0]
- Idempotenz für kritische Endpunkte gefordert? [J/N] → bei J: "Welche Endpunkte? Warum?"
- Ziel-Latenz (p95) kritisch? [J/N] → bei J: "Welche Grenzen (ms)?"

Checks:
- Wenn Writes ≥ Reads/2 → **Storage/Index/Queue-Bedarf** markieren.

### 3) Batch-Verarbeitung
- Regelmäßige Batches? [J/N] → bei J:
  - Records pro Lauf: [K/M/G/T]
  - Daten pro Lauf: **GB/TB** (Freitext)
  - Max. Laufzeit kritisch? [J/N] → bei J: "SLO (min/h)?"
  - Feste Zeitfenster? [J/N] → bei J: "Wann/Zeitzone?"

Checks:
- Wenn Laufzeit > 50% Fenster → **Sharding/Parallelisierung** vorschlagen.

### 4) Streaming & Events (pro Tag)
- Event-Frequenz gesamt: [K/M/G/T/0]
- Event-Größe relevant? [J/N] → bei J: "Ø KB / Max KB?"
- Exactly-once Semantik gefordert? [J/N] → bei J: "Für welche Flüsse?"
- Fanout > 1 Konsument? [J/N] → bei J: "Ø/Max Abnehmer pro Event?"

Checks:
- Exactly-once + hoher Fanout → **Komplexitäts-/Kosten-Flag** setzen.

### 5) Datenbestände & Änderungen
- Persistenter **Heiß**-Bestand (online): **GB/TB** (Freitext) + Klassifikation [K/M/G/T]
- Warm/Kalt/Archiv relevant? [J/N] → bei J: "Größen (GB/TB) und Retention (Tage/Monate/Jahre)?"
- Neue Daten pro Tag (Records): [K/M/G/T/0]
- Änderungsrate hoch (>10%/Tag)? [J/N] → bei J: "Geschätzter Anteil %?"

Checks:
- Warm+Kalt ≫ Heiß → **Tiering/ILM** vorschlagen.

### 6) Integrationen & Limits
- Externe Upstreams mit Rate Limits? [J/N] → bei J: "Welche Quoten/SLAs?"
- Downstreams mit Quoten/Backpressure? [J/N] → bei J: "Welche?"
- DLQ/Retry-Politik notwendig? [J/N] → bei J: "Backoff-Strategie?"

Checks:
- Externes Rate Limit < erwartete RPH → **Puffer/Queue/Circuit Breaker** fordern.

### 7) Peaks, Saisonalität & Wachstum
- Starke **Saisonalität** (z. B. Monatsende, Kampagnen)? [J/N] → bei J: "Wann/Größe/Dauer?"
- **Peaks/Spikes** (außergewöhnlich)? [J/N] → bei J: "Trigger/Größe/Dauer?"
- **Wachstum 12–24 Monate** signifikant? [J/N] → bei J: "Faktor in K/M/G/T je Dimension?"
- **Kapazitätsziel**: Planung auf p95 × **Sicherheitsfaktor** = [1.5/2/3] (Auswahl)

### 8) Qualitäts-/Betriebsziele (workload-bezogen)
- Verfügbarkeitssziel (>99.9%)? [J/N] → bei J: "Ziel in %?"
- Recovery-Ziele streng (RPO/RTO < 1h)? [J/N] → bei J: "Konkret (min)?"
- Hohe Cache-Hitrate angestrebt? [J/N] → bei J: "% (Warm/Kaltstart)"

### 9) Kostenrahmen
- Cloud-Kosten kritisch? [J/N] → bei J: "Welche Dimension (Compute/Storage/Network)?"
- Cost-per-X wichtig? [J/N] → bei J: "Welche X (1k Requests, 1 Mio Events, GB/Monat)?"

## Transformation → `context/workload.md`
Nach dem Interview generiere:
- **Zusammenfassung** (Bulletpoints je Block)
- **Klassifikation** je Dimension (K/M/G/T/0) **und** abgeleitete grobe Zahlen (Heuristik)
- **Annahmen & Quellen** (mit Datum)
- **Risiken & Implikationen** (automatische Flags aus Checks)

Dateiaufbau:
```md
# Project Workload

## Summary
- Concurrency: M (≈ …)
- Reads RPH: K …
…

## Details
### Nutzer & Concurrency
Antworten + Begründungen …

### Requests pro Stunde (RPH)
…

### Batch
…

### Streaming & Events
…

### Datenbestände & Änderungen
…

### Integrationen & Limits
…

### Peaks, Saisonalität & Wachstum
…

### Qualitäts-/Betriebsziele
…

### Kostenrahmen
…

## Annahmen & Quellen
- …
