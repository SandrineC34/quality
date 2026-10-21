# Planification de la démarche Qualité

https://drive.google.com/drive/folders/13gqUSQL27wA3v0zHUq4Cuwbf73H2EXkZ




https://www.leblogdudirigeant.com/twos/


    Stratégie Offensive (Forces/Opportunités)
    Stratégie Défensive (Faiblesses/Menaces)
    Stratégie de Veille (Forces/Menaces)
    Stratégie de moyen et long terme (Faiblesses/Opportunités)

# Creation d'un token d'authorisation



# Modification d'un fichier
les cases modifiables sont entouré de orange lorsque l'on clique desus
## Modification d'un élément
    cliquer sur la case à modifier
    modifier le test
    enregistrer
## Ajout d'un élément 
cliquer sur la case à modifier, 
cliquer sur entrée
## Suppression d'une case
cliquer sur la case à supprimer 
cliquer sur tab arrière pour vider la case


## Creation d'un token
Le Personal Access Token (PAT) est votre mot de passe d'API sécurisé. Chaque collaborateur qui a le droit de modifier les documents doit générer le sien depuis son compte GitLab en suivant ces étapes :

    Connectez-vous sur votre compte GitLab : https://forge.inrae.fr/OpenSILEX/Quality

    Dans le menu de gauche, cliquez sur  Settings (Paramètres).

    Dans le menu déroulant  cliquez sur Access Tokens (Jetons d'accès).

    Cliquez sur le bouton Add new token (Ajouter un nouveau jeton).

    Remplissez les champs :

        Token name : Donnez un nom clair (ex: Modification-SMQ-sc).

        Expiration date : Laissez vide ou mettez une date lointaine.

        Select a role : Developer

        Scopes (Droits d'accès) : Cochez impérativement la case write_repository (c'est elle qui autorise le script à enregistrer les modifications).

    Cliquez sur Create personal access token.

    Attention : Copiez immédiatement le token qui s'affiche à l'écran (il ressemble à une longue suite de lettres et chiffres comme glpat-xxxxxxxxxxxx). Il ne s'affichera qu'une seule fois. C'est ce code qu'il faudra coller dans la boîte de dialogue sur votre page web.

## Sécurisation de la branch principale (main) pour sécurisation des validations

1. Bloquer la branche principale (main) dans l'interface de GitLab

Pour empêcher le script (ou un utilisateur) d'écraser la branche principale directement, vous devez la "protéger".

    Allez sur votre projet sur le site web de GitLab.

    Dans le menu de gauche, allez dans Settings ⚙️ > Repository.

    Déroulez la section Protected branches (Branches protégées).

    Repérez la branche main (ou ajoutez-la si elle n'y est pas) et configurez-la ainsi :

        Allowed to merge : Maintainers (Les administrateurs / Responsables Qualité).

        Allowed to push : No one (Personne, ce qui bloque l'écriture directe du script).

    Cliquez sur Protect.

    Pour les rôles des personnes 
    Owner pour les responsables
    Maintener pour les pilotes 
    Develloper pour les autres collaborateurs

## Restriction des éléments suivant le status

Restreindre la modification de certains dossiers (Le fichier CODEOWNERS)

Si vous voulez aller plus loin et interdire à certaines personnes de soumettre des modifications sur des processus spécifiques (par exemple : seul le service RH peut modifier les documents RH, seuls les développeurs peuvent modifier le fichier Developpement.html), GitLab propose la fonctionnalité Code Owners.

Dans votre dépôt (via VS Code), créez un fichier nommé exactement CODEOWNERS à la racine de votre projet. Vous pouvez y écrire des règles comme ceci :
Plaintext

Chemin du fichier ou dossier           Compte(s) GitLab autorisé(s)

# Chemin du fichier ou dossier           # Compte(s) GitLab autorisé(s)

# Ajout de plusieurs personnes (ex: Anne, isabelle)
/html/Processus/Management/              @anne.tireau @isabelle.alic

# Déjà configuré avec plusieurs personnes
/html/Processus/Metier/Developpement.html @pilote.dev @sandrine.c

/html/Politique/                         @responsable.qualite

on peut aussi creer des groupes exemple :
management
exploitation
developpement

Comment cela se comporte avec votre bouton web ?

Si un utilisateur qui n'est pas listé dans le fichier CODEOWNERS tente de modifier la page Management.html et clique sur le bouton d'enregistrement :

    Le script va créer la branche et la Merge Request.

    Cependant, GitLab va bloquer automatiquement la fusion tant qu'elle n'aura pas été validée et signée électroniquement par la personne désignée dans le fichier CODEOWNERS (ici @anne.tireau).
## S'assurer que la vm dispose toujours de version validée

Lorsque le script s'exécute, il envoie les données directement chez GitLab. Il ne modifie pas les fichiers localement sur le disque dur de la VM. La VM n'est qu'un "lecteur" du dépôt.

Pour que votre VM affiche toujours la version officielle validée, configurez une tâche automatisée (Cron) sur la VM pour aller chercher les nouveautés de GitLab à intervalles réguliers (toutes les heures ou toutes les nuits par exemple).

Sur le terminal de votre VM :

    Positionnez-vous dans le dossier du projet.

    Configurez une tâche planifiée qui exécute la commande suivante :
    Bash

    git pull origin main

Résultat final pour votre SMQ :

    L'utilisateur modifie la page à l'écran et clique sur Enregistrer.

    Sur l'écran : Rien ne change pour les autres tant que ce n'est pas validé.

    Sur GitLab : Une Merge Request propre apparaît. Le Responsable Qualité vérifie le texte en vert/rouge, valide et clique sur Merge.

    Sur la VM : Au prochain git pull, le serveur récupère la version finale approuvée et la met à disposition de toute l'entreprise. C'est 100 % conforme à l'ISO 9001.

## Attention droits d'accès
le depot quality est dans opensilex, qui est dispose de trop de personne, prevoir une migration vers un nouveau edpot
