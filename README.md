# 🏰 Système d'Information Patrimonial Urbain (SIPU)

<p align="center">
  <img src="https://img.shields.io/badge/École-FST%20Tanger-blue?style=for-the-badge&logo=academic" alt="FST Tanger">
  <img src="https://img.shields.io/badge/Filière-Géoinformation-green?style=for-the-badge&logo=map" alt="GéoInfo">
  <img src="https://img.shields.io/badge/Cours-Admin%20Réseaux%20%26%20OS-orange?style=for-the-badge&logo=linux" alt="OS">
</p>

<p align="center">
  <strong>Un projet complet d'ingénierie : De la conception Merise au déploiement Cloud.</strong>
</p>

---

## 📖 Présentation

Ce dépôt contient l'intégralité du projet de **Gestion du Patrimoine Urbain**. Il a pour but de moderniser le suivi des monuments historiques en centralisant les données techniques, administratives et géographiques au sein d'un système unique.

Le projet est structuré pour suivre rigoureusement le cycle de vie d'un logiciel, depuis l'analyse conceptuelle jusqu'à l'implémentation technique.

---

## 📂 Structure du Dépôt

L'organisation des fichiers suit la méthodologie **MERISE**, garantissant une traçabilité complète de la conception.

| Dossier | Description | Contenu |
| :--- | :--- | :--- |
| **🗂️ MCC** | Modèle Conceptuel de Communication | Diagrammes de flux entre les acteurs (Service Municipal, Prestataires). |
| **🧠 MCD** | Modèle Conceptuel de Données | Schémas Entité-Association (Bâtiments, Inspections, Zones). |
| **⚙️ MCT** | Modèle Conceptuel de Traitements | Diagrammes des processus métier (Validation travaux, Inspections). |
| **📋 MOT** | Modèle Organisationnel de Traitements | Répartition des tâches (Homme vs Machine). |
| **🔄 MLD** | Modèle Logique de Données | Traduction du MCD en schéma relationnel (Clés étrangères). |
| **💾 MPD** | Modèle Physique de Données | Scripts de création des tables PostgreSQL. |
| **💻 ui-app** | **Application Web (Code Source)** | Le code Python/Flask complet. **(Voir README interne)** |
| **🔍 requetes_SQL** | Analyses de Données | Requêtes SQL complexes pour les statistiques (Question 10). |

---

## 🛠️ Stack Technologique

Le projet s'appuie sur des technologies robustes et open-source :

* **Conception :** Méthode Merise.
* **Base de Données :** PostgreSQL 16 + **PostGIS** (Extension Spatiale).
* **Backend :** Python 3.10 (Flask Framework).
* **Frontend :** Bootstrap 5 + Jinja2.
* **Cartographie :** Leaflet.js.
* **Déploiement :** Railway (App) + Neon (Database).

---

## 🚀 Installation et Démonstration

### Pour lancer l'application :
Toute la documentation technique, l'installation des dépendances (`requirements.txt`) et le guide de démarrage se trouvent dans le dossier dédié :

👉 **[Accéder au dossier `ui-app`](./ui-app)**

### Documents de référence :
Les spécifications complètes et le rapport final sont disponibles à la racine :
* `Mini-Projet géoinformation_2025-2026.pdf` (Cahier des charges)

---

## 👥 Auteurs

Projet réalisé par les étudiants ingénieurs de la **FST Tanger** :

* **Mohammed Belfellah** ([@MohammedBelfellah](https://github.com/MohammedBelfellah))
* **Hamza Boulahrouf** ([@Hamza-7bl](https://github.com/Hamza-7bl))

---

<p align="center">
  <i>Année Universitaire 2024-2025</i>
</p>
