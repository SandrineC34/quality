/**
 * Constantes propres au module "Suivi des actions".
 * Regroupe les actions issues des non-conformités, des revues de direction,
 * des audits ou de toute autre origine, avec suivi de l'efficacité (ISO 9001 §10).
 */

/* Origine de l'action */
export const ORIGINES = [
  "Non-conformité",
  "Revue de direction",
  "Audit interne",
  "Audit externe",
  "Réclamation client",
  "Autre",
];

/* Type d'action (ISO 9001 distingue ces catégories) */
export const TYPES_ACTION = ["Corrective", "Préventive", "Amélioration"];

export const PRIORITES = ["Faible", "Moyenne", "Haute"];

/* Statut saisi manuellement. "En retard" est aussi recalculé automatiquement
   à l'affichage (voir utils/suiviActions.js -> isEnRetard) tant que l'action
   n'est pas clôturée, pour éviter un statut qui se périme. */
export const STATUTS_ACTION = ["À faire", "En cours", "En retard", "Clôturée"];
export const STATUT_FILTER_OPTIONS = ["Tous les statuts", ...STATUTS_ACTION];

/* Résultat de la mesure d'efficacité */
export const RESULTATS_EFFICACITE = [
  "Non évaluée",
  "Efficace",
  "Partiellement efficace",
  "Non efficace",
];

/* Colonnes du tableau principal */
export const ACTIONS_TABLE_COLUMNS = [
  "N° réf",
  "Date création",
  "Origine",
  "Type",
  "Descriptif de l'action",
  "Responsable",
  "Date prévue",
  "Statut",
  "Date clôture",
  "Efficacité",
];

/* Mapping statut -> classes de couleur (badges) */
export const STATUT_STYLES = {
  "À faire": "bg-slate-100 text-slate-700",
  "En cours": "bg-blue-100 text-blue-700",
  "En retard": "bg-red-100 text-red-700",
  "Clôturée": "bg-emerald-100 text-emerald-700",
};

export const EFFICACITE_STYLES = {
  "Non évaluée": "bg-slate-100 text-slate-500",
  "Efficace": "bg-emerald-100 text-emerald-700",
  "Partiellement efficace": "bg-amber-100 text-amber-700",
  "Non efficace": "bg-red-100 text-red-700",
};
