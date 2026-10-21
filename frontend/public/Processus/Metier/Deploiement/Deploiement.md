---
id: P2-04
titre: Déploiement applicatif
sous_titre: Validation · Déploiement · Vérification post-déploiement
badge: deploy
badge_texte: P2-04 Déploiement applicatif
pilote: À définir (co-pilotage Infrastructure / Développement recommandé)
participants: Administrateurs Systèmes, Responsable développement, Équipe exploitation
version: 1.0
date: /10/2026
titre_page: Processus Déploiement applicatif P2-04 - OpenSILEX
---

## Sous-processus
- SP1 Déploiement et mise en production | validation pré-déploiement, déploiement via CI/CD, vérification post-déploiement, notification

## Mode de pilotage
- SP1: Validations de release avant déploiement en production
- SP1: Pipeline GitLab CI/CD (traçabilité automatique)
- SP1: Registre des instances déployées

## Finalité
Déployer de manière maîtrisée, documentée et traçable les releases et correctifs applicatifs (OpenSILEX, SilexExplorer) produits par le Développement (P2-02), en garantissant la validation des prérequis avant mise en production, la conformité aux standards de configuration et la notification des équipes concernées.

## Parties prenantes
- Développement (P2-02) — fournisseur des artefacts
- Infrastructure & MCO (P2-03) — fournisseur de l'environnement
- Accompagnement des communautés (P2-01) — destinataire de la notification
- Management (P1-01)
- Utilisateurs finaux

## Interactions

### Développement (P2-02) | Amont
- entrée SP1: Packages applicatifs, artefacts de déploiement (release / hotfix), tag Git, changelog

### Infrastructure & MCO (P2-03) | Amont
- entrée SP1: Environnement de déploiement configuré et disponible
- sortie SP1: Anomalies d'environnement identifiées lors de la vérification post-déploiement

### Exploitation (P2-01) | Aval
- sortie SP1: Notification de mise à disposition effective de l'instance / release

### Management (P1-01) | Amont
- entrée SP1: Roadmap, planification des releases

## Documentation
- SP1: Registre des instances déployées (liste instances)
- SP1: Pipelines GitLab CI/CD (templates de déploiement)
- SP1: Templates Ansible de configuration
- SP1: Procédure de validation pré-déploiement (check-list)
- SP1: Procédure de rollback

## Ressources
- Humaines: Pilote (à désigner), administrateurs systèmes, responsable développement
- Outils: GitLab CI/CD, Ansible (templates de configuration), registre des instances
- Environnements: Préproduction, production (infrastructure gérée par P2-03)

## Activités principales

### SP1 | D1. Validation et déploiement
Réception des artefacts de déploiement (release ou hotfix) depuis le Développement (P2-02). Vérification de la complétude des spécifications (changelog, tag Git, notes de version) et validation des prérequis de l'environnement cible (disponibilité infrastructure, conformité configuration). Déploiement via GitLab CI/CD et Ansible selon les templates de configuration, avec validation formelle documentée avant toute mise en production.

### SP1 | D2. Vérification post-déploiement et notification
Tests de bon fonctionnement du service déployé (connectivité, accès, services applicatifs). En cas d'anomalie : retour en correction avec le Développement (P2-02) ou l'Infrastructure (P2-03) selon la nature du problème, et redéploiement. Notification à l'Exploitation (P2-01) de la mise à disposition effective. Documentation du déploiement dans le registre des instances.

## Objectifs
- Obj1 | SP1 | Déployer de manière maîtrisée, documentée et transparente pour les utilisateurs les releases et correctifs applicatifs. | satisfaction
- Obj2 | SP1 | Garantir la traçabilité complète de chaque déploiement (artefact, environnement, validations, notifications). | confiance, risque

## KPI
- Obj1 | Taux de déploiements validés avant mise en production | 100 % | Mensuel | (Instances déployées avec validation documentée / Total instances déployées) × 100. Source : registre des instances.
- Obj1 | Taux de déploiements réalisés via pipeline automatisé (CI/CD) | ≥ 90 % | Trimestriel | (Déploiements via GitLab CI/CD ou Ansible / Total déploiements) × 100. Source : GitLab.
- Obj2 | Délai moyen entre réception artefact et notification exploitation | À définir | Par release | Temps entre réception du tag Git et notification à P2-01. Source : suivi interne / GitLab.

## Risques
- R1 | SP1 | Déploiement non maîtrisé ou sans validation | Instance déployée sans validation préalable des spécifications ou sans respect des standards de configuration, entraînant des dysfonctionnements en production. | Valider formellement les prérequis avant mise en production et déployer uniquement via GitLab CI/CD et Ansible avec traçabilité dans le registre des instances.
- R2 | SP1 | Artefact incomplet ou non conforme reçu du Développement | Un artefact livré sans changelog complet, sans tag Git ou sans notes de version rend la validation impossible et peut entraîner des régressions. | Check-list de réception formalisée ; retour systématique vers P2-02 si l'artefact est incomplet avant tout déploiement.
- R3 | SP1 | Environnement cible non disponible ou non conforme | L'infrastructure nécessaire au déploiement n'est pas prête (VM non créée, configuration manquante), bloquant la mise en production. | Coordination préalable avec P2-03 ; vérification des prérequis environnement avant déclenchement du pipeline.
- R4 | SP1 | Absence de procédure de rollback opérationnelle | En cas d'anomalie post-déploiement, l'absence de procédure de retour arrière prolonge l'indisponibilité du service. | Maintenir et tester une procédure de rollback documentée pour chaque type de release.

## KRI
- R1 | Taux de déploiements avec retour en correction | ≤ 10 % | Trimestriel | (Déploiements avec retour en correction ou rollback / Total déploiements) × 100. Source : registre des instances / GitLab.
- R2 | Nombre d'artefacts reçus incomplets (sans changelog, sans tag Git) | 0 | Par sprint | Décompte des artefacts refusés à réception pour non-conformité. Source : suivi interne.
- R3 | Nombre de déploiements bloqués faute d'environnement disponible | 0 | Trimestriel | Décompte des pipelines en attente d'environnement au-delà du délai prévu. Source : GitLab.

## Opportunités
- O1 | SP1 | Automatisation des déploiements comme levier de fiabilité | L'extension de l'automatisation via Ansible et GitLab CI/CD réduit les erreurs humaines, accélère la mise en production et renforce la traçabilité des configurations. |

## KIO
- O1 | Taux de déploiements réalisés via pipeline automatisé | ≥ 95 % d'ici fin d'exercice | Trimestriel | (Déploiements via CI/CD / Total déploiements) × 100. Cible progressive : renforcement de l'automatisation.

## Indicateurs de fonctionnement
- SP1 | Nombre d'instances déployées | Décompte des instances applicatives déployées en production. Source : GitLab CI / registre de déploiement. | Trimestriel
- SP1 | Nombre de hotfixes déployés | Décompte des correctifs urgents déployés hors cycle de release standard. Source : GitLab / JIRA. | Par sprint
- SP1 | Nombre de releases déployées | Décompte des versions majeures/mineures mises en production. Source : GitLab. | Trimestriel

## Logigramme SP1
- entrée: Artefacts release / hotfix (tag Git · changelog · notes de version) depuis P2-02
- étape [D1]: D1 — Validation & déploiement | Vérification complétude artefact · vérification prérequis environnement · déploiement Ansible/GitLab CI/CD · validation documentée
- décision: Service opérationnel ? | non | Nature du problème ?
  
- étape: D2 — Vérification post-déploiement & notification | Tests fonctionnels · mise à jour registre instances · notification Exploitation P2-01
- sortie: Instance déployée · Exploitation notifiée · registre mis à jour