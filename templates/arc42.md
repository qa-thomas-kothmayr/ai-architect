# arc42 Architektur-Dokumentation

## Metadata

* **System:** `<system_name>`
* **Version:** `<version>`
* **Generiert:** `<timestamp>`
* **Agent:** `<agent_id>`
* **Status:** `<draft|review|approved>`

---

## 1. Einführung und Ziele

* **Aufgabenstellung:** `<primary_purpose>`
* **Qualitätsziele:** `<performance, security, usability, maintainability>`
* **Stakeholder:** `<role: concerns>`

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

## 5. Bausteinsicht

### Ebene 1 - System Overview
* **Komponenten:** `<component_name: responsibility>`
* **Schnittstellen:** `<interface_name: protocol>`

### Ebene 2 - Container Detail
* **Container:** `<container_name: technology, purpose>`
* **Abhängigkeiten:** `<dependency_graph>`

### Ebene 3 - Component Detail
* **Komponenten:** `<internal_components[]>`
* **Implementierung:** `<implementation_details>`

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