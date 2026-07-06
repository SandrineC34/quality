/** Constantes du module de suivi des indicateurs qualité (ISO 9001) */

export const FREQUENCES = ["Mensuelle", "Trimestrielle", "Semestrielle", "Annuelle"];
export const METHODES_CALCUL = ["Moyenne", "Somme", "Dernière valeur"];
export const SENS_CIBLE = ["Plus est mieux", "Moins est mieux"];
export const UNITES = ["%", "Nb", "Jours", "Heures", "k€", "Autre"];
export const STATUTS = ["Atteint", "À surveiller", "Non atteint"];

export const STATUT_FILTER_OPTIONS = ["Tous les statuts", ...STATUTS];

/** Libellés des champs de saisie selon la fréquence de collecte choisie */
export const PERIOD_LABELS = {
  Mensuelle: ["Jan", "Fev", "Mar", "Avr", "Mai", "Juin", "Juil", "Aout", "Sep", "Oct", "Nov", "Dec"],
  Trimestrielle: ["T1", "T2", "T3", "T4"],
  Semestrielle: ["S1", "S2"],
  Annuelle: ["Valeur annuelle"],
};

/** Badges de couleur par statut (vert = atteint, orange = à surveiller, rouge = non atteint) */
export const STATUT_STYLES = {
  Atteint: "bg-emerald-100 text-emerald-700",
  "À surveiller": "bg-amber-100 text-amber-700",
  "Non atteint": "bg-red-100 text-red-700",
};

export const INDICATEUR_TABLE_COLUMNS = [
  "Processus",
  "Réf. interne",
  "Réf. ISO",
  "Description",
  "Unité",
  "Cible",
  "Fréquence",
  "Résultat annuel",
  "Écart vs cible",
  "Statut",
  "Responsable",
  "Commentaires",
];

/** Suggestions de processus déjà rencontrés (le champ reste un texte libre) */
export const PROCESSUS_SUGGESTIONS = [
  "Management",
  "RH / Compétences",
  "Ressources",
  "Production / Réalisation",
  "Achats",
  "Client",
];