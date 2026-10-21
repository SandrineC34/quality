---
id: P2-02
titre: Développement
sous_titre: Conception · Développement · Tests · Corrections de bugs · Scripts
badge: dev
badge_texte: P2-02 Développement
pilote: Responsable de l'équipe de développement
participants: Développeurs, Testeurs
version: 3.0
date: /10/2026
titre_page: Processus Développement P2-02 - OpenSILEX
---

## Sous-processus
- SP1 Cycle de développement | conception (phase conditionnelle), développement, tests, corrections de bugs, scripts, release

> **Note Conception.** La Conception (maquettes UX/UI, spécifications fonctionnelles et techniques, analyse de faisabilité) n'est plus un sous-processus séparé. Elle constitue une **phase d'entrée conditionnelle** du SP1, activée sur critère de complexité (nouveau domaine fonctionnel, impact architectural, demande utilisateur complexe). Cette intégration reflète la réalité opérationnelle — le logigramme de l'ancien SP2 démarrait lui-même par la question « Conception activée ? » — et simplifie les interfaces JIRA.

## Mode de pilotage
- SP1: Réunions Agile/Scrum : mêlée quotidienne, planification, rétrospective
- SP1: Tableau de suivi JIRA (backlog, sprints, bugs)
- SP1: Revues de conception formelles avant démarrage du développement (si phase Conception activée)

## Finalité
Concevoir, produire et faire évoluer les solutions logicielles (OpenSILEX, SilexExplorer) et les outils de traitement de données associés, en garantissant la qualité, la sécurité, la maintenabilité du code et la conformité aux besoins fonctionnels et techniques.

## Parties prenantes
- Équipe de développement
- Équipe d'exploitation (P2-01)
- Déploiement applicatif (P2-04)
- Management (P1-01)
- Utilisateurs finaux
- Utilisateurs métiers (si phase Conception activée)

## Interactions

### Management (P1-01) | Amont
- entrée SP1: Cartes JIRA priorisées, roadmap et allocation des ressources
- entrée SP1: Décisions de validation ou rejet des demandes
- entrée SP1: Plan de gestion des données (PGD), PGL
- sortie SP1: Demandes d'arbitrage, plannings de sprint
- sortie SP1: KPI développement (avancement, qualité, bugs)

### Exploitation (P2-01) | Amont & aval
- entrée SP1: Cartes JIRA priorisées (bugs qualifiés, fonctionnalités, améliorations)
- entrée SP1: Contexte utilisateur, contraintes métier
- entrée SP1 (Conception): Expression du besoin, cahier des charges
- entrée SP1 (Conception): Retours sur maquettes et prototypes
- sortie SP1: Cartes JIRA mises à jour (avancement, correction)
- sortie SP1: Outils de scripting
- sortie SP1 (Conception): Spécifications fonctionnelles et techniques, maquettes UX/UI validées

### Déploiement applicatif (P2-04) | Aval
- sortie SP1: Nouvelle version / hotfix / release (artefacts de déploiement, tag Git, changelog)

## Documentation
- SP1: Guide de rédaction des user stories
- SP1: Standards de codage OpenSILEX
- SP1: Procédure de merge request
- SP1: Guide d'utilisation de Git et de la forge INRAE
- SP1: Grille de tests d'intégration
- SP1: Procédure de versionnement (semantic versioning)
- SP1: Documentation technique (API, architecture)
- SP1: Procédure de correction de bug
- SP1 (Conception): Guide de conception UX/UI
- SP1 (Conception): Modèles de maquettes
- SP1 (Conception): Grille d'analyse de faisabilité et d'estimation de charge
- SP1 (Conception): Templates de spécifications fonctionnelles et techniques

## Ressources
- Humaines: Responsable équipe développement, développeurs, testeurs
- Outils: JIRA (backlog, sprints, bugs), Git / forge INRAE (versionnement), IDE, outils d'analyse statique du code
- Environnements: Développement, préproduction, production (géré par Infrastructure P2-03)
- Conception: Outils de maquettage UX/UI, templates de spécifications

## Activités principales

### SP1 — Phase Conception (conditionnelle) | C1. Analyse des besoins et conception fonctionnelle
*Déclencheur : carte JIRA complexe (nouveau domaine fonctionnel, impact architectural, demande utilisateur significative).*
Formalisation des besoins en exigences fonctionnelles (contraintes, rétrocompatibilité, interopérabilité), conception des maquettes UX/UI et présentation à l'Exploitation. La validation formelle conditionne le passage à C2 ; tout refus donne lieu à une itération documentée.

### SP1 — Phase Conception (conditionnelle) | C2. Conception technique
Étude comparative des solutions, vérification de la cohérence avec l'architecture existante d'OpenSILEX et SilexExplorer, identification des composants et dépendances. Validation par le Management si impact stratégique, puis entrée en cycle de développement.

### SP1 | D1. Planification du sprint
Sélection des cartes JIRA (nouvelles fonctionnalités, bugs, scripts) ou des spécifications issues de la phase Conception, estimation de la charge, répartition des tâches et définition des objectifs du sprint. Temporalité : toutes les 3–4 semaines.

### SP1 | D2. Développement, corrections de bugs et scripts
Implémentation du code (OpenSILEX, SilexExplorer) selon les spécifications ou la demande directe, respect des standards de codage, rédaction et exécution des tests unitaires automatiques, corrections de bugs en préproduction et production, développement des outils de scripting à la demande, versionnement Git. Temporalité : boucle de sprint.

### SP1 | D3. Documentation technique
Documentation du code (commentaires, javadoc), mise à jour de la documentation de l'architecture si nécessaire, rédaction des notes techniques pour les évolutions majeures et documentation des API modifiées ou créées. Temporalité : pour chaque développement.

### SP1 | D4. Revue de code
Création d'une merge request, revue par un pair, vérification de la qualité et des bonnes pratiques, corrections des remarques, validation et fusion dans la branche de développement. Temporalité : pour chaque développement.

### SP1 | D5. Tests d'intégration
Exécution des tests d'intégration automatisés et des tests fonctionnels manuels sur la branche intégrée. En cas d'échec, retour en D2 avec corrections documentées. Temporalité : pour chaque développement.

### SP1 | D6. Préparation Release ou Hotfix
Création du tag Git, génération des artefacts de déploiement et rédaction des notes de version (changelog). Transmission au processus Déploiement applicatif (P2-04) pour mise en production ou correctif urgent (hotfix). Temporalité : à chaque hotfix ou release.

## Objectifs
- Obj1 | SP1 | Produire un logiciel (OpenSILEX, SilexExplorer) conforme aux spécifications fonctionnelles et techniques, en garantissant la qualité, la maintenabilité et la sécurité du code livré. Corriger les bugs identifiés en préproduction et production dans les délais. | satisfaction, risque
- Obj2 | SP1 | Garantir la mise à disposition des outils de scripting de traitement des données à la demande. | satisfaction
- Obj3 | SP1 — Phase Conception | Traduire les besoins qualifiés par l'Exploitation en spécifications fonctionnelles et techniques exploitables. Concevoir les maquettes UX/UI et l'architecture applicative pour les demandes complexes, afin de réduire les allers-retours coûteux en développement. | satisfaction

## KPI
- Obj1 | Délai moyen de correction de bugs | ≤ 3 jours | Par sprint | Moyenne du temps entre signalement et correction d'un bug. Source : JIRA / Mantis.
- Obj2 | Délai moyen de mise à disposition d'un outil de scripting | ≤ 15 jours ouvrés | Semestriel | Moyenne du nombre de jours ouvrés entre la validation de la demande (carte JIRA) et la mise à disposition de l'outil au demandeur. Source : JIRA / suivi interne.
- Obj3 | Taux d'évolutions significatives livrées sans retour en conception | ≥ 85 % | Trimestriel | (Nb d'évolutions significatives livrées sans remise en cause des spécifications pendant le développement / Nb total d'évolutions significatives livrées) × 100 — mesuré uniquement si phase Conception activée. Source : JIRA.

## Risques
- R1 | SP1 | Accumulation de la dette technique et manque de documentation | Code mal structuré, non maintenu ou documenté de manière obsolète, ralentissant l'évolution des logiciels et la transmission des compétences. | Allocation systématique de 10 à 15 % du temps de sprint au refactoring et à la mise à jour de la documentation ; contrôle automatisé SonarQube.
- R2 | SP1 | Problèmes de performance | Lenteur détectée par l'utilisateur, impactant l'expérience d'utilisation d'OpenSILEX ou SilexExplorer. | Mise en place de tests de charge avant chaque release majeure.
- R3 | SP1 | Non-qualité logicielle (régressions et bugs en production) | Défauts et régressions non détectés en phase de test, impactant la stabilité et la confiance des utilisateurs. | Obligation de couverture de tests unitaires, revue de code par les pairs avant merge, intégration continue automatisée.
- R4 | SP1 | Mauvaise planification des sprints ou mauvaise priorisation | Les objectifs de sprint ne sont pas atteints dans les délais, désorganisant la planification globale. | Planification entre développeurs puis validation par l'exploitation ; allocation de 5 à 10 % de temps de sprint pour les urgences.
- R5 | SP1 | Introduction de failles de sécurité dans le code | Utilisation de dépendances à risques ou obsolescence de celles-ci. | Veille technologique, analyse des dépendances.

## KRI
- R1 | Taux des MR de fonctionnalités qui induisent l'ajout ou la mise à jour de la documentation | ≥ 80 % | Trimestriel | (Nb de merges avec mise à jour / Nb total de merges) × 100
- R2 | Temps de réponse moyen des services | ≤ 2 s | Mensuel | Temps moyen de réponse des requêtes principales mesuré en production (outil de monitoring)
- R3 | Couverture de code par les tests | ≥ 70 % | Version majeure/mineure | % de code couvert par les tests unitaires
- R3 | Taux de régressions détectées après déploiement | ≤ 5 % des livraisons | Version majeure | (Nb de livraisons ayant généré une régression en production / Nb total de livraisons) × 100
- R3 | Nombre de bugs remontés en production | ≤ 5 / mois | Mensuel | Nombre de bugs remontés en production après déploiement. Source : JIRA / Mantis.
- R4 | Taux de complétion des sprints | ≥ 85 % | Par sprint | (Nb de user stories complétées / Nb de user stories planifiées) × 100
- R5 | Taux de dépendances qui présentent des failles de sécurité connues | À définir | Par sprint | (Nb de dépendances à risques / Nb total de dépendances) × 100

## Indicateurs de fonctionnement
- SP1 | Nombre de cartes JIRA traitées | Décompte des cartes passées au statut « terminé » dans le mois. Source : JIRA. | Par sprint
- SP1 | Nombre de merge requests validées | Décompte des merge requests approuvées et fusionnées. Source : forge INRAE / GitLab. | Par sprint
- SP1 | Nombre de releases publiées | Décompte des tags de version créés (release). Source : GitLab. | Trimestriel
- SP1 | Nombre de hotfixes publiés | Décompte des correctifs urgents déployés hors cycle de release. Source : Git / JIRA. | Par sprint
- SP1 | Nombre d'outils de scripting mis à disposition | Décompte des outils de scripting livrés à la demande. Source : suivi interne. | Semestriel
- SP1 | Revue de processus | Réalisation de la revue de processus annuelle | Annuel
- SP1 | Nombre de phases Conception activées | Décompte des demandes ayant déclenché la phase Conception (C1/C2). Source : JIRA. | Trimestriel

## Logigramme SP1

### Entrée : déclenchement
- entrée: Carte JIRA validée (bug, fonctionnalité, script)
- décision: Phase Conception activée ? | critère : complexité, nouveau domaine, impact architectural
  - oui → Phase Conception C1/C2
  - non → D1 Planification directe

### Phase Conception (conditionnelle)
- étape [C1]: Analyse des besoins & conception fonctionnelle | Exigences · maquettes UX/UI · présentation Exploitation · collecte retours
- décision: Validation fonctionnelle ? | non | Itération documentée | retour C1
- étape [C2]: Conception technique | Solutions techniques · architecture · dépendances · validation Management si impact stratégique
- sortie phase: Spécifications fonctionnelles · maquettes · architecture validée → D1

### Cycle de développement
- étape: D1 — Planification du sprint | Sélection cartes JIRA · estimation charge · répartition tâches · objectifs sprint
- étape [D2]: D2 — Développement & tests unitaires | Implémentation · standards codage · tests auto · correction bugs · scripts · Git
- étape: D3 — Documentation technique | Commentaires code · javadoc · notes techniques · API modifiées ou créées
- étape: D4 — Revue de code | Merge request · revue pair · vérification bonnes pratiques · corrections · validation
- décision: Tests d'intégration OK ? | non | Correction | ↻ retour D2
- étape: D6 — Préparation Release ou Hotfix | Tag Git · artefacts de déploiement · changelog · notes de version
- sortie: Artefact · tag Git · changelog → P2-04 Déploiement applicatif