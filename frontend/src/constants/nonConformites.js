/**
 * Constantes propres au module "Non-conformités".
 * Une autre page (ex: Indicateurs) aura son propre fichier
 * dans ce dossier (ex: constants/indicateurs.js) sans toucher à celui-ci.
 */

/* Listes déroulantes du formulaire NC */
export const SOURCES = ["Audit interne", "Client", "Fournisseur", "Réclamation", "Interne"];
export const SERVICES = ["Management", "Production", "Qualité", "Achats", "Logistique", "RH", "Commercial"];
export const GRAVITES = ["Mineure", "Majeure", "Critique"];
export const STATUTS = ["Ouverte", "En cours", "Clôturée"];
export const ACTION_STATUTS = ["À faire", "En cours", "Abandonnée", "Reportée"];
export const STATUT_FILTER_OPTIONS = ["Tous les statuts", ...STATUTS];

/* Colonnes du tableau des NC */
export const NC_TABLE_COLUMNS = [
  "N° réf",
  "Date de détection",
  "Détecté par",
  "Processus impacté",
  "Description de la non-conformité",
  "Gravité",
  "Action immédiate",
  "Analyse des causes",
  "Actions correctives", 
  "Statut", 
  "Date clôture",
  "Preuves/commentaire"
  ];

/* Mapping statut -> classes de couleur (badges) */
export const STATUT_STYLES = {
  Ouverte: "bg-orange-100 text-orange-700",
  "En cours": "bg-blue-100 text-blue-700",
  Clôturée: "bg-emerald-100 text-emerald-700",
};

export const ACTION_STATUT_STYLES = {
  "À faire": "bg-slate-100 text-slate-700",
  "En cours": "bg-blue-100 text-blue-700",
  Abandonnée: "bg-red-100 text-red-700",
  Reportée: "bg-amber-100 text-amber-700",
};
