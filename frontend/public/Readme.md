# Charte Graphique 
# ===================
'''
Ananalyse des couleurs OpenSilex

**Logo & Plateforme OpenSILEX**

L'identité visuelle d'OpenSILEX (système d'information pour le phénotypage des plantes et la gestion des données scientifiques) s'articule autour d'une palette moderne orientée data et agronomie :

    Bleu Cyan / Tech (Actif & Accent) :

        Code Hex : #0096D6 (ou #00A8E8 / #17A2B8)

        RGB : rgb(0, 150, 214)

        Usage : Éléments interactifs, boutons, liens et puces du logo.

    Bleu Marine Silex (Structure & Fond sombre) :

        Code Hex : #1E293B (ou #0F172A)

        RGB : rgb(30, 41, 59)

        Usage : En-têtes, textes principaux et structures du portail.

    Vert Feuille / Agronomie (Secondaire) :

        Code Hex : #4CAF50

        RGB : rgb(76, 175, 80)


    Analyse des couleurs du logo MISTEA :

    Jaune / Orange (Début d'arc) : #F2B200 (ou #EBB012)

    Vert Clair / Lime (Feuille) : #82C325 (ou #70C128)

    Vert Émeraude / Moyen : #00A389

    Vert Foncée / Canard (Texte MISTEa) : #0A423C (ou #103B38)



Récapitulatif Palette pour vos projets CSS/Design


::root {
  /* --- LOGO MISTEA --- */
  --mistea-yellow:       #F2B200; /* Arc jaune/orange */
  --mistea-lime:         #82C325; /* Feuille vert clair */
  --mistea-green:        #00A389; /* Vert émeraude */
  --mistea-dark-green:   #0A423C; /* Couleur du texte "MISTEa" */
  
  /* Dégradé de l'arc MISTEA */
  --mistea-gradient: linear-gradient(135deg, #F2B200 0%, #82C325 35%, #00A389 70%, #0A423C 100%);

  /* --- INRAE / MATHNUM --- */
  --inrae-green-primary: #00A389;
  --inrae-green-dark:    #275662;

  /* --- OPENSILEX --- */
  --opensilex-blue:      #0096D6;
  --opensilex-dark-navy: #1E293B;
  --opensilex-leaf-green:#4CAF50;

  /* --- COULEURS NEUTRES --- */
  --bg-light:            #F8FAFC;
  --text-main:           #0A423C;
}


**

  exemple :

  Couleur primaire (Vert OpenSILEX)
    --primary-color: #5ebc7e;
    --primary-dark: #4a9d63;
    --primary-darker: #3d8654;
    --primary-darkest: #2f6b42;
    --primary-light: #7cd39a;
    --primary-lighter: #a9dfbf;
    --primary-lightest: #d5f4e6;
    --primary-ultralight: #e8f8f0;
  
  UTILISATION :
  1. Inclure ce fichier dans toutes les pages HTML :
     <link rel="stylesheet" href="charte.css">
  
  2. Utiliser les variables dans les CSS :
     background: var(--primary-color);
     border-radius: var(--border-radius-lg);
  
  3. Pour modifier la charte graphique, Modifiez les valeurs dans charte.css
'''


# Dockerisation de l'application
# ==============================








# Evolution Possible
# ===================

Etape n°1

La page d'acceuil peut avoir des options de connexions:
  1. connexion en tant qu'invité
  2. connexion en tant qu'administeur


  - l'invité aura accès à une nombre limité de pages
  - l'administrateur aura accès à l'ensemble des pages


Etape n°2

  - Permettre à l'administrateur de modifier les pages via l'interface web

Etape n°3

  - Ajouter des pages "métier" pour remplcer les excel actuels 
  - Bases de données et sauvegarde




# Gestion des saut de page

<!-- Forcer un saut de page AVANT cette section -->
<div class="section page-break-before">
  <h2>Cette section commence sur une nouvelle page</h2>
  ...
</div>

<!-- Forcer un saut de page APRÈS cette section -->
<div class="section page-break-after">
  <h2>Nouvelle page après cette section</h2>
  ...
</div>

<!-- Autoriser la coupure d'une section très longue -->
<div class="section allow-break">
  <h2>Cette section peut être coupée si trop longue</h2>
  ...
</div>

# Exemple

<!-- Le logigramme sur sa propre page -->
<div class="section page-break-before page-break-after">
  <h2>🔀 Logigramme du processus</h2>
  <iframe src="Manag-log.html" ...></iframe>
</div>

<!-- Les risques peuvent être coupés si trop longs -->
<div class="section allow-break">
  <h2>⚠️ Analyse des risques</h2>
  <table class="risk-table">...</table>
</div>

<!-- Les KPI sur une nouvelle page -->
<div class="section page-break-before">
  <h2>📊 Indicateurs de performance (KPI)</h2>
  ...
</div>

# Pour les tableaux (les En-tête se répetent sur chaque page)

<table class="risk-table">
  <thead>
    <tr>
      <th>Risque</th>
      <th>Impact</th>
      <th>Probabilité</th>
    </tr>
  </thead>
  <tbody>
    <!-- Vos lignes ici -->
  </tbody>
</table>



&#x2190;  <!-- flèche gauche -->
&#x2191;  <!-- flèche haut -->
&#x2192;  <!-- flèche droite -->
&#x2193;  <!-- flèche bas -->
&#x21D2;  <!-- double flèche droite -->


# Definition des indicateurs

1. KPI — Key Performance Indicator (Indicateur de Performance Clé)

Définition : Mesure l'atteinte d'un résultat attendu par rapport à un objectif fixé (SMART). Il répond à la question : "Est-ce qu'on atteint nos objectifs ?"

Caractéristiques :

Toujours associé à un objectif mesurable et à une cible chiffrée
Regard rétrospectif (constate ce qui a été produit)
Alimente la revue de direction (§9.1.3 ISO 9001)
Sert au pilotage stratégique et à la prise de décision

Exemple sur ce processus : Taux de succès des demandes de financement ≥ 40 %

2. KRI — Key Risk Indicator (Indicateur de Risque Clé)

Définition : Signal d'alerte précoce sur une dérive potentielle ou un risque en train de se matérialiser. Il répond à la question : "Y a-t-il un signal qui annonce un problème à venir ?"

Caractéristiques :

Regard prospectif (anticipe, surveille)
Déclenche une action corrective avant que le KPI ne se dégrade
Lié à un risque identifié (§6.1 ISO 9001)
Le dépassement d'un seuil = alerte, pas encore un échec

Exemple sur ce processus : Taux de diffusion des décisions dans les délais < 95 % → alerte sur un dysfonctionnement de communication avant que les parties prenantes n'en subissent les conséquences

3. KIO — Key Initiative/Opportunity Indicator (parfois appelé KOI)

Définition : Mesure l'avancement d'une initiative stratégique ou opportunité (jalon, projet, démarche). Il répond à la question : "Où en est-on dans la réalisation d'une action stratégique ?"

Caractéristiques :

Temporaire par nature (s'éteint à la fin de l'initiative)
Pilote un plan d'action ou une opportunité identifiée (§6.1)
Non récurrent, contrairement au KPI

Exemple (en commentaire dans le fichier) : Avancement du dossier de labellisation ISC — jalon d'une démarche ponctuelle

4. Indicateur de Fonctionnement

Définition : Mesure l'activité courante d'un processus, sans valeur décisionnelle directe. Il répond à la question : "Que s'est-il passé ? Combien ?"

Caractéristiques :

Descriptif, pas normatif (pas de cible stratégique)
Utile pour le suivi opérationnel quotidien
Ne doit pas figurer dans le tableau de bord de pilotage — section "Information"
Alimente les statistiques d'activité et les rapports de fond

Exemple : Nombre de COPIL tenus dans l'année, Nombre de non-conformités ouvertes