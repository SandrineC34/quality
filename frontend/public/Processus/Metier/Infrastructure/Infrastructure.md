---
id: P2-03
titre: Infrastructure & MCO
sous_titre: Création d'infrastructure · Maintien en Condition Opérationnelle · Supervision · PRA
badge: infra
badge_texte: P2-03 Infrastructure & MCO
pilote: Renaud Colin
participants: Pilote du processus, Administrateurs Systèmes, SI central, Équipe exploitation, Direction / Management
version: 3.0
date: /10/2026
titre_page: Processus Infrastructure & MCO P2-03 - OpenSILEX
---

## Sous-processus
- SP1 Création d'infrastructure | création et configuration de VMs, configuration réseau, sécurité et certificats
- SP2 MCO & Supervision | supervision avancée, MCO continu, sauvegardes, PRA, iRODS, iDRAC

> **Note périmètre.** Le déploiement des services applicatifs (releases, hotfixes) est désormais traité dans le processus dédié **P2-04 Déploiement applicatif**. P2-03 couvre exclusivement la création et le maintien de l'infrastructure technique sous-jacente.

## Mode de pilotage
- SP1: Réunions techniques fin de sprint
- SP2: Tableaux de bord Prometheus / Grafana
- SP2: Alertes automatisées Mattermost
- SP2: Exercices PRA planifiés (annuels)

## Finalité
Garantir la disponibilité, la sécurité et la performance de l'infrastructure technique hébergeant les services OpenSILEX. Le processus couvre la création et la configuration des machines virtuelles, le maintien en condition opérationnelle (supervision, sauvegardes, gestion des incidents) et le plan de reprise d'activité (PRA).

## Parties prenantes
- Pilote du processus
- Administrateurs Systèmes
- SI central
- Déploiement applicatif (P2-04)
- Équipe exploitation (P2-01)
- Utilisateurs finaux
- Utilisateurs iRODS/S3 & Stockage
- Direction / Management
- Tutelles / DSI

## Interactions

### Management (P1-01) | Amont
- entrée SP1: Roadmap, allocation ressources, PGD / PGL
- entrée SP2: Plan infrastructure PRA, MCO
- sortie SP2: Rapports d'incidents, tableaux de bord disponibilité

### Déploiement applicatif (P2-04) | Amont & aval
- entrée SP2: Alertes incidents liés aux instances déployées
- sortie SP1: Environnement technique disponible pour le déploiement
- sortie SP2: État de supervision des instances

### Exploitation (P2-01) | Aval
- sortie SP2: Alertes incidents, état supervision

### SI central / Tutelles / DSI | Amont
- entrée SP1: Quotas de ressources disponibles, contraintes de sécurité
- sortie SP1: Cahier des charges fonctionnel, inventaire CMDB

### Utilisateurs iRODS/S3 | Aval
- entrée SP2: Demandes de comptes, signalement d'incidents iRODS
- sortie SP2: Comptes configurés, infra iRODS opérationnelle

## Documentation
- SP1: Formulaire de demande de VM / CR réunion
- SP1: Standards de configuration (templates Ansible)
- SP1: Guide de dimensionnement des ressources
- SP1: Standards de sécurité et durcissement
- SP1: Documentation réseau (plan d'adressage, VLAN, firewall)
- SP1: Registre des certificats SSL/TLS
- SP2: Tableaux de bord Grafana / Prometheus
- SP2: Documentation iRODS (architecture, comptes, quotas)
- SP2: Plan de Reprise d'Activité (PRA)
- SP2: Politiques de sauvegarde (RPO / RTO)

## Ressources
- Humaines: Pilote (Renaud Colin), administrateurs systèmes, SI central
- Matérielles: Serveurs physiques, VMs, réseau (VLAN, firewall, bastion), stockage iRODS, iDRAC
- Supervision: Prometheus / Grafana (métriques), Mattermost (alertes), runbooks
- Sauvegardes & PRA: Outils de sauvegarde (VM, BDD, fichiers critiques), environnement de secours
- Déploiement infrastructure: Ansible (templates de configuration), registre des certificats SSL/TLS

## Activités principales

### SP1 | I1. Réception, analyse et dimensionnement
Réception de la demande de création de VM, échange avec le demandeur pour qualifier les besoins techniques (CPU, RAM, stockage, OS). Évaluation de la faisabilité et des ressources disponibles, dimensionnement de l'architecture (IP, DNS, VLAN) et planification de la mise en œuvre avec estimation du délai de livraison.

### SP1 | I2. Création, configuration et sécurisation de la VM
Création de la VM et allocation des ressources, installation de l'OS, configuration du réseau (IP, DNS, firewall) et application des standards de sécurité et de durcissement. Installation des agents de monitoring de base, configuration des accès et droits, mise à jour de l'inventaire CMDB. Tests de connectivité réseau, d'accès (SSH, certificats) et de performances validés avant livraison.

### SP1 | I3. Livraison, documentation et support utilisateur
Rédaction de la documentation complète (IP, ports, accès, services) et transmission du dossier au processus MCO (SP2). Notification aux parties prenantes. Pour les utilisateurs iRODS : création des comptes avec droits appropriés, configuration des quotas et transmission sécurisée des credentials.

### SP2 | M1. Intégration et supervision avancée
Réception du dossier de livraison SP1 et vérification de sa complétude. Configuration des sondes de monitoring avancées (CPU, RAM, disque, réseau, services applicatifs, logs, métriques métier), définition des seuils d'alerte (warning / critical) et des notifications Mattermost. Création des tableaux de bord Grafana, tests des alertes et documentation de la configuration de supervision.

### SP2 | M2. Surveillance continue et maintenance préventive
Monitoring permanent des tableaux de bord, analyse des alertes et intervention selon les runbooks. Maintenance préventive planifiée : patches de sécurité, mises à jour, renouvellement des certificats SSL/TLS, nettoyage des logs et optimisation des performances. Surveillance de l'utilisation des ressources et anticipation des saturations.

### SP2 | M3. Sauvegardes, incidents et PRA
Définition et configuration de la politique de sauvegarde (RPO, RTO, fréquence, rétention) selon le type (VM complète, bases de données, fichiers critiques), planification des tâches et tests initiaux de restauration. Gestion des incidents : détection automatique ou signalement utilisateur, qualification (criticité, impact, urgence), diagnostic, application du runbook et restauration du service documentée. Tests trimestriels de restauration sur environnement de test et exercices PRA annuels (simulation de sinistre, mesure RTO/RPO réels, amélioration continue du plan).

## Objectifs
- Obj1 | SP1 | Livrer aux utilisateurs des VM sécurisées, conformes à leurs besoins fonctionnels et prêtes à l'emploi. | satisfaction, risque
- Obj2 | SP2 | Assurer la disponibilité des services, les sauvegardes/PRA, la gestion du stockage (iRODS/S3, iDRAC) et garantir l'assistance aux utilisateurs. | satisfaction, confiance

## KPI
- Obj1 | Taux de VM documentées complètement | 100 % | Mensuel | (VM avec documentation complète / Total VM livrées) × 100
- Obj1 | Taux de VM conformes aux standards de sécurité à la livraison | 100 % | Trimestriel | (VM validées sur la check-list durcissement / Total VM livrées) × 100
- Obj2 | Disponibilité de l'infrastructure | ≥ 99 % | Trimestriel | (Temps total − Temps d'indisponibilité) / Temps total × 100
- Obj2 | Taux de succès des sauvegardes | ≥ 98 % | Mensuel | (Sauvegardes réussies / Total sauvegardes planifiées) × 100

## Risques
- R1 | SP1 | Saturation des ressources | CPU, RAM ou stockage atteignent leurs limites, dégradant les performances ou empêchant la création de nouvelles VM sans arbitrage préalable. | Surveiller les seuils de capacité, revoir les quotas chaque trimestre avec le SI central et valider les ressources avant toute création de VM.
- R2 | SP2 | Incident (iRODS, Instance) | Plateforme ou instance devenant indisponible ou perdant des données, impactant la gestion des données de recherche. | Appliquer les runbooks, maintenir la supervision et les sauvegardes, tirer un retour d'expérience après chaque incident majeur.
- R3 | SP2 | Défaillance de la supervision | Défaillance de l'infrastructure détectée par les utilisateurs avant d'être identifiée par les outils de supervision. | Tester les alertes à la mise en service, supprimer toute VM non supervisée du périmètre livré.
- R4 | SP1 | Documentation incomplète ou absente | La VM est livrée sans documentation adéquate, compliquant la maintenance et le dépannage futurs. | Rendre la check-list de documentation obligatoire en I3 et contrôler la complétude du dossier à la réception par le MCO.
- R5 | SP2 | Échec du PRA | Le plan de reprise d'activité n'est pas testé ou ne fonctionne pas en situation réelle, prolongeant l'indisponibilité. | Planifier un exercice PRA annuel et des tests de restauration trimestriels, avec un plan d'actions correctives suivi jusqu'à clôture.
- R6 | SP2 | Non-respect du RTO / RPO | Le temps de restauration ou la perte de données dépasse les objectifs définis, impactant la continuité de service. | Définir RTO / RPO par service, les mesurer lors des tests et ajuster fréquence et rétention des sauvegardes en cas d'écart.
- R7 | SP2 | Défaillance du système de sauvegarde | Les sauvegardes ne sont pas effectuées, échouent ou sont corrompues, empêchant la restauration des données. | Alerter automatiquement sur tout échec de sauvegarde et vérifier l'intégrité par des tests de restauration trimestriels.

## KRI
- R1 | Taux d'utilisation des quotas | ≤ 85 % | Trimestriel | (Ressources utilisées / Ressources totales disponibles) × 100
- R2 | Nombre d'incidents majeurs | 0 | Mensuel | Incidents avec indisponibilité supérieure au RTO ou perte de données
- R3 | Taux d'incidents détectés par les utilisateurs | ≤ 15 % | Mensuel | (Nb d'incidents détectés par les utilisateurs / Nb total d'incidents) × 100
- R4 | Nombre de VM sans documentation complète depuis plus de 30 jours | 0 | Mensuel | Décompte des VM livrées dont la documentation reste incomplète 30 jours après livraison
- R5 | Résultat de l'exercice PRA (RTO mesuré vs RTO cible) | RTO mesuré ≤ RTO cible | Annuel | Temps de restauration mesuré lors de l'exercice PRA comparé au RTO cible
- R6 | Nombre d'incidents dépassant le RTO cible | 0 | Mensuel | Décompte des restaurations dont la durée dépasse le RTO du service concerné
- R7 | Nombre de VM avec 2 échecs de sauvegarde consécutifs | 0 | Mensuel | Décompte des VM dont les 2 dernières sauvegardes planifiées ont échoué

## Opportunités
- O1 | SP2 | PRA testé comme argument de confiance partenaires | Un PRA documenté et régulièrement exercé constitue un critère différenciant pour les partenaires scientifiques et les tutelles, renforçant la confiance dans la continuité de service d'OpenSILEX. |

## Indicateurs de fonctionnement
- SP1 | Nombre de VMs créées | Décompte des nouvelles VMs mises en service. Source : CMDB / inventaire. | Trimestriel
- SP1 | Nombre de certificats SSL/TLS renouvelés | Décompte des certificats renouvelés dans l'année. Source : registre des certificats. | Annuel
- SP1 | Nombre de mises à jour de patches de sécurité appliquées | Décompte des patches appliqués sur les VMs en production. Source : rapports maintenance préventive. | Mensuel
- SP2 | Nombre d'incidents traités | Décompte des incidents enregistrés et clôturés dans le mois. Source : Prometheus / journal incidents. | Mensuel

## Logigramme SP1
- entrée: Demande de VM · spécifications techniques
- étape: I1 — Réception, analyse & dimensionnement | Qualification besoin · faisabilité · architecture IP/DNS · planification
- étape [I2]: I2 — Création, configuration & sécurisation VM | OS · réseau · sécurité · monitoring de base · accès · CMDB
- décision: Tests validés ? | non | Correction | ↻ retour I2
- étape: I3 — Livraison, documentation & support utilisateur | Documentation complète · transmission MCO · comptes iRODS · notification
- sortie: VM livrée · dossier transmis → SP2 MCO

## Logigramme SP2
- entrée: Dossier de livraison SP1 · alertes incidents
- étape: M1 — Intégration & supervision avancée | Sondes monitoring · seuils d'alerte · Grafana · tests alertes · documentation
- étape: M2 — Surveillance continue & maintenance préventive | Monitoring tableaux de bord · patches · certificats · capacité ressources
- décision: Incident détecté ? | oui | Gestion incident | Runbook · restauration
- étape: M3 — Sauvegardes, tests restauration & PRA | Politique RPO/RTO · tests trimestriels · exercices PRA annuels
- sortie: Infrastructure supervisée · PRA à jour · incidents résolus