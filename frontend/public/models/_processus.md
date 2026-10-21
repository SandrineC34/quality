---
# ═══ MODÈLE DE PROCESSUS ═══  (copier ce fichier, le renommer, ex : Support.md, puis lancer : python build.py)
# Les lignes de cette zone : clé: valeur
id: P3-O1
titre: Nom du processus
sous_titre: Thème 1 · Thème 2 · Thème 3
badge: mgmt                       # suffixe de la classe CSS badge-xxx (mgmt, infra, ...)
badge_texte: P3-O1 Nom du processus
pilote: Prénom Nom
participants: Pilote, Équipe X, Direction
version: 1.0
date: 10/2026
# titre_page: (optionnel, sinon = titre)
---

<!--
  RÈGLES
  • Le séparateur de colonnes est " | " (espace, barre, espace).
  • Les sous-processus sont numérotés dans l'ordre : le 1er = SP1, le 2e = SP2, etc.
  • Chaque ligne "- ..." = une ligne de tableau / une puce. Autant de lignes que vous voulez.
  • Une section vide ou supprimée n'apparaît pas dans la page.
  • Les commentaires <!-- ... --> sont ignorés.
-->

## Sous-processus
<!-- Titre | Périmètre -->
- Premier sous-processus | ce qu'il couvre
- Deuxième sous-processus | ce qu'il couvre
- Troisième sous-processus | ce qu'il couvre

## Mode de pilotage
- SP1: Réunion ...
- SP2: Tableau de bord ...

## Finalité
Un paragraphe (peut tenir sur plusieurs lignes).

## Parties prenantes
- Partie prenante 1
- Partie prenante 2

## Interactions
<!-- ### Nom du processus ou acteur | Rôle (Amont / Aval / Amont & aval)
     puis autant de lignes entrée / sortie que nécessaire -->

### Processus X (P1-O1) | Amont & aval
- entrée SP1: Donnée reçue
- sortie SP2: Donnée produite

### Acteur externe | Amont
- entrée SP1: Demande

## Documentation
<!-- SPn: texte  (le préfixe SPn colore la ligne ; sans préfixe = neutre) -->
- SP1: Document A
- SP2: Document B

## Ressources
<!-- Catégorie: contenu -->
- Humaines: ...
- Outils: ...
- Environnements: ...

## Activités principales
<!-- ### SPn | Titre   puis un paragraphe. Numérotation 1, 2, 3… automatique. -->

### SP1 | Première activité
Description de l'activité.

### SP1 | Deuxième activité
Description.

### SP2 | Activité du sous-processus 2
Description.

## Objectifs
<!-- Obj | SP | Description | politiques (séparées par des virgules) -->
- Obj1 | SP1 | Description de l'objectif | confiance, satisfaction
- Obj2 | SP2 | Description de l'objectif | amelioration

## KPI
<!-- Obj | Indicateur | Cible | Fréquence | Mode de calcul    (le SP est déduit de l'objectif) -->
- Obj1 | Nom de l'indicateur | ≥ 80 % | Trimestriel | (A / B) × 100
- Obj2 | Nom de l'indicateur | ≤ 5 % | Annuel | (A / B) × 100

## Risques
<!-- N° | SP | Risque | Description | Actions de maîtrise -->
- R1 | SP1 | Titre du risque | Description | Mesure préventive
- R2 | SP2 | Titre du risque | Description | Mesure préventive

## KRI
<!-- Risque | Indicateur | Cible | Fréquence | Mode de calcul -->
- R1 | Indicateur d'alerte | ≤ 85 % | Mensuel | Formule
- R1 | Un 2e indicateur pour le même risque | ≤ 5 | Mensuel | Formule
- R2 | Indicateur d'alerte | ≥ 95 % | Mensuel | Formule

## Opportunités
<!-- N° | SP | Titre | Description | Mesure de surveillance (peut rester vide) -->
- O1 | SP1 | Titre | Description |

## KIO
<!-- Opportunité | Indicateur | Cible | Fréquence | Mode de calcul -->
- O1 | Indicateur | ≥ 2 / an | Annuel | Décompte

## Indicateurs de fonctionnement
<!-- SP | Indicateur | Définition | Fréquence -->
- SP1 | Nombre de ... | Décompte des ... | Mensuel

## Logigramme SP1
<!--
  - entrée: texte
  - étape [A1]: Titre | sous-titre            ([A1] = identifiant facultatif, nécessaire seulement pour un retour)
  - décision: Question ? | non | Titre de la boîte | sous-titre | retour A1
        2e champ  : branche qui part sur le côté (oui ou non) ; l'autre branche continue vers le bas
        dernier champ "retour A1" : facultatif → trace une flèche de retour vers l'étape A1
                                    (sans retour : la boîte est une fin « refus / abandon »)
  - sortie: texte
-->
- entrée: Déclencheur
- étape [A1]: Titre de l'étape | Détail · détail · détail
- décision: Conforme ? | non | Correction | Reprise de l'étape | retour A1
- étape [A2]: Titre de l'étape | Détail
- sortie: Résultat livré

## Logigramme SP2
- entrée: Déclencheur
- étape: Titre de l'étape | Détail
- sortie: Résultat livré
