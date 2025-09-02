# arc42 Architektur-Dokumentation

## Metadata (PFLICHT)

* **System:** `<system_name>`
* **Version:** `<version>`
* **Generiert:** `<timestamp>` (ISO 8601: YYYY-MM-DD HH:MM:SS)
* **Agent-Version:** Claude Code v{version} + arc42
* **Source-Dokumente:** [design/structure.md](../design/structure.md), [design/selections.md](../design/selections.md), [context/domain.md](../context/domain.md)
* **Status:** `Entwurf|Review|Genehmigt`
* **Completeness-Check:** `✅ Vollständig | ⚠️ Unvollständig | 🔄 In Bearbeitung`

---

## 1. Einführung und Ziele (PFLICHT, min. 200 Wörter)

**Aufgabenstellung (PFLICHT):** Primärer Zweck und Geschäftsziele des Systems
*Beispiel-Inhalt:* Das E-Commerce-System ermöglicht Online-Produktverkauf mit integrierter Bestellabwicklung...

**Qualitätsziele (PFLICHT):** 
- 🟢 Performance: <100ms Antwortzeit
- 🟢 Security: HTTPS, Verschlüsselung
- 🟡 Usability: Intuitive Benutzerführung
- 🟢 Maintainability: Modulare Architektur

**Stakeholder (PFLICHT):** 
- Endkunden: Einfache Produktsuche und Kaufabwicklung
- Betrieb: Skalierbare, wartbare Infrastruktur
- Entwicklungsteam: Erweiterbare Architektur

**Cross-References:**
→ Siehe auch: [Kontext](03-kontextabgrenzung.md)
→ Bezug zu: [Domain-Anforderungen](../context/domain.md)

---

## 2. Randbedingungen

* **Technische Randbedingungen:** `<technologies[], platforms[], frameworks[]>`
* **Organisatorische Randbedingungen:** `<team_structure, processes, deadlines>`
* **Konventionen:** `<coding_standards, naming_conventions, documentation_rules>`

---

## 3. Kontextabgrenzung

* **Fachlicher Kontext:** `<business_partners[], external_systems[]>`
* **Technischer Kontext:** `<interfaces[], protocols[], data_formats[]>`

---

## 4. Lösungsstrategie

* **Technologieentscheidungen:** `<technology: rationale>`
* **Architekturmuster:** `<patterns[], architectural_styles[]>`
* **Qualitätsziele-Umsetzung:** `<quality_goal: approach>`

---

## 5. Bausteinsicht (PFLICHT, min. 300 Wörter)

**Diagramm-Referenz:** [Baustein-Diagramm](05-bausteinsicht.mmd)

### Ebene 1 - System Overview (PFLICHT)
**Hauptkomponenten (min. 3):**
- Frontend-App: Benutzerinteraktion und Präsentation  
- API-Gateway: Service-Orchestrierung und Authentifizierung
- Core-Services: Geschäftslogik-Implementation
- Datenschicht: Persistierung und Caching

**Schnittstellen:**
- REST APIs: JSON über HTTPS
- Event-Bus: Asynchrone Service-Kommunikation

### Ebene 2 - Container Detail (optional)
**Container-Architektur:**
- Web-Container: React SPA
- API-Container: Node.js/Express Services  
- DB-Container: PostgreSQL Cluster

**Cross-References:**
→ Details in: [Laufzeitsicht](06-laufzeitsicht.md)
→ Deployment: [Verteilungssicht](07-verteilungssicht.md)

---

## 6. Laufzeitsicht

* **Szenarien:** `<scenario_name: flow_description>`
* **Sequenzen:** `<interaction_flows[]>`
* **Zustandsübergänge:** `<state_transitions[]>`

---

## 7. Verteilungssicht

* **Deployment-Einheiten:** `<deployment_units[]>`
* **Infrastruktur:** `<infrastructure_components[]>`
* **Mapping:** `<software_component → hardware_node>`

---

## 8. Querschnittliche Konzepte

* **Fachliche Konzepte:** `<domain_models[], business_rules[]>`
* **User Experience:** `<ui_patterns[], interaction_concepts[]>`
* **Sicherheit:** `<authentication, authorization, encryption>`
* **Architektur-/Design-Muster:** `<patterns[], anti_patterns[]>`

---

## 9. Architekturentscheidungen

* **Verwandte ADRs:** `<adr_ids[]>`
* **Entscheidungsübersicht:** `<decision: status, rationale>`

---

## 10. Qualitätsanforderungen

* **Qualitätsbaum:** `<quality_attributes_hierarchy>`
* **Szenarien:** `<quality_scenario: metric, test_approach>`

---

## 11. Risiken und technische Schulden

* **Risiken:** `<risk_id: probability, impact, mitigation>`
* **Technische Schulden:** `<debt_item: priority, effort_estimate>`

---

## 12. Glossar

* **Begriffe:** `<term: definition>`
* **Abkürzungen:** `<abbreviation: expansion>`

---

## Agent-Instruktionen

* **Diagramm-Format:** mermaid
* **Namenskonventionen:** camelCase
* **Abstraktionsebene:** medium
* **Validierungsregeln:** `<completeness_check, consistency_validation, cross_reference_integrity>`

---

## Anhänge

* **Referenzen:** `<external_docs[], standards[]>`
* **Vorlagen:** `<template_references[]>`