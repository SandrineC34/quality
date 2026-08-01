# User Stories — Module Gestion des Non-conformités, Réclamations et Anomalies (incident Qualité)


### US-NC-01 — Déclarer un incident Qualité

**En tant que** Responsable Qualité ou Pilote de processus,
**je veux** ouvrir une fiche de "non-conformité" en décrivant l'incident constaté,
**afin de** tracer l'incident dès sa détection, quelle que soit son origine (interne, fournisseur, client, réclamation).

**Critères d'acceptation :**
- La date de détection et la description de l'anomalie sont obligatoires
- Je peux préciser le canal de détection (source), le processus impacté
- La fiche est enregistrée avec un statut initial par défaut
- Un numéro de référence est attribué automatiquement à la fiche

---

### US-NC-02 — Qualifier et analyser les causes

**En tant que** Responsable Qualité ou Pilote de processus,
**je veux** compléter une fiche NC avec une classification et une analyse des causes,
**afin de** comprendre l'origine du dysfonctionnement avant de définir un plan de traitement.

**Critères d'acceptation :**
- Je peux renseigner une analyse des causes en texte libre
- Je la possibilité d'avoir ne méthode structurée guidée — 5 pourquoi, Ishikawa à la demande 
- Je peux classifier la typologies de l'incident (Anomalie, non conformité, Ecart)
- Je peux indiquer la gravité (Majeur, mineur, critique)
- Je peux modifier cette analyse à tout moment tant que la fiche n'est pas clôturée
- Je peux Demander des suggestion d'analyse en fonction de mon contexte par un agent IA

---

### US-NC-03 — Enregistrer une action curative immédiate

**En tant que** Pilote de processus,
**je veux** renseigner l'action curative réalisée pour corriger l'anomalie dans l'immédiat,
**afin de** distinguer la correction ponctuelle du traitement de fond (action corrective).
a trancher doit on mettre le nom de la personne ayant fait l'action pour la tracabilité

**Critères d'acceptation :**
- Je peux saisir une description de l'action curative et sa date de réalisation
- Ce champ est distinct des actions correctives/préventives de fond
- Ces informations restent modifiables tant que la fiche n'est pas clôturée

---

### US-NC-04 — Ajouter une ou plusieurs actions correctives/préventives

**En tant que** Responsable Qualité,
**je veux** rattacher une ou plusieurs actions correctives ou préventives à une fiche NC,
**afin de** traiter la cause de fond et éviter la récurrence de l'anomalie.

**Critères d'acceptation :**
- Je peux ajouter autant d'actions que nécessaire (0 à N)
- Chaque action a : un type (corrective, préventive, amélioration), une description, un pilote responsable, une échéance et un statut
- Je peux supprimer une action non encore validée
- le pilote de l'action doit-il être sélectionné dans une liste d'utilisateurs (à creer par ailleurs)

---

### US-NC-05 — Suivre le statut d'une action corrective

**En tant que** Pilote d'action ou Responsable Qualité,
**je veux** faire évoluer le statut d'une action corrective au fil de son traitement,
**afin de** piloter son avancement jusqu'à sa clôture.

**Critères d'acceptation :**
- Le statut par défaut d'une nouvelle action est « À faire »
- Si je renseigne une date de clôture sur une action, son statut passe automatiquement à « Clôturée »
les statuts intermédiaires possibles — ex. « En cours », « En retard »,« Abandonnée », « Reportée » 

---

### US-NC-06 — Clôturer une fiche de non-conformité

**En tant que** Responsable Qualité,
**je veux** clôturer une fiche NC une fois le traitement terminé,
**afin de** garantir que l'anomalie a été traitée et vérifiée avant archivage.

**Critères d'acceptation :**
- Si je renseigne une date de clôture sur la fiche, son statut passe automatiquement à « Clôturée »
- la clôture doit-elle être bloquée tant qu'une action corrective rattachée n'est pas elle-même clôturée
- La vérification de d'efficacité Programmé dans le suivi des action n'a pas d'influence sur la cloture de la fiche de non conformité

---

### US-NC-07 — Modifier une fiche de non-conformité existante

**En tant que** Responsable Qualité ou Pilote de processus,
**je veux** rouvrir et modifier une fiche NC existante,
**afin de** corriger ou compléter les informations tout au long du traitement.

**Critères d'acceptation :**
- Je peux cliquer sur une fiche existante pour l'ouvrir en modification
- Les données affichées sont une copie de travail : rien n'est modifié tant que je n'ai pas validé
- le responsable qualité peut modifier des fiches de non conformité ouverte ou cloturée , le pilote de processus peut uniquement modifier une fiche de non conformité non cloturée.
- La suppression d'action est interdite pour le pilote, le responsable qualité peut supprimer une action en justifiant la raison et cela doit etre tracable.

---

### US-NC-08 — Consulter la liste des non-conformités

**En tant que** Pilote de processus, Responsable Qualité ou Direction,
**je veux** consulter la liste de toutes les non-conformités,
**afin de** avoir une vue d'ensemble de l'état des anomalies et de leur traitement.

**Critères d'acceptation :**
- Le tableau affiche a minima : référence, date, source, processus impacté, description, gravité, statut, date de clôture, nb d'action rattachée
- Un message dédié s'affiche si aucune fiche n'existe encore
- Un incicateur visuel permet de voir l'avancement de clôture des actions
- tri des colonnes, filtres par statut/processus/gravité, pagination pour un grand volume de fiches à definir

---

### US-NC-09 — Consulter les actions rattachées à une non-conformité

**En tant que** Responsable Qualité ou Pilote de processus,
**je veux** déplier une fiche NC pour voir le détail de ses actions correctives,
**afin de** suivre leur avancement sans ouvrir chaque action individuellement.

**Critères d'acceptation :**
- Un indicateur affiche le nombre d'actions rattachées à une fiche
- Le clic sur cet indicateur déplie un sous-tableau détaillant chaque action (référence, type, description, pilote, échéance, date de clôture, statut)
- Le dépliage déclenche  l'ouverture du formulaire de modification de la fiche

---

### US-NC-10 — Restreindre l'accès selon le profil utilisateur *(non implémenté à ce jour)*

**En tant que** Administrateur ou Responsable Qualité,
**je veux** que les droits de création, modification, clôture et suppression des NC soient limités selon le profil de l'utilisateur connecté,
**afin de** garantir l'intégrité du processus qualité (cf. EB-4, matrice des droits par profil).

**Critères d'acceptation :**
- Un Contributeur peut déclarer une NC et consulter, mais pas clôturer ni supprimer
- Un Pilote de processus peut agir uniquement sur les NC de son ou ses processus
- Seul un Responsable Qualité peut clôturer ou supprimer une fiche
- Le contrôle est appliqué côté serveur (API), pas uniquement par masquage d'interface

---

### US-NC-11 — Rattacher une non-conformité à son origine *(à confirmer, non implémenté à ce jour)*

**En tant que** Responsable Qualité,
**je veux** relier une fiche NC à l'audit, la réclamation client ou le processus dont elle est issue,
**afin de** conserver la traçabilité de son origine et faciliter les analyses transverses (cf. EB-3.2 et EB-3.4).

**Critères d'acceptation :**
- *(à trancher : ce lien est-il un simple champ de référence libre, ou une relation structurée vers les modules Audits/Réclamations une fois ces modules développés ?)*

---

## Récapitulatif

| ID | User story | Statut de développement |
|---|---|---|
| US-NC-01 | Déclarer une NC |
| US-NC-02 | Qualifier et analyser les causes |
| US-NC-03 | Action curative immédiate |
| US-NC-04 | Ajouter des actions correctives |
| US-NC-05 | Statut d'une action |
| US-NC-06 | Clôturer une NC |
| US-NC-07 | Modifier une NC |
| US-NC-08 | Consulter la liste des NC |
| US-NC-09 | Consulter les actions rattachées |
| US-NC-10 | Droits d'accès par profil |
| US-NC-11 | Rattachement à l'origine |

*Ce document sert de base pour rédiger ou compléter les fiches fonctionnelles détaillées (SFD) correspondantes.