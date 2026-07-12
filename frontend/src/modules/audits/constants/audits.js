/**
 * Constantes propres au module "Planification des audits internes".
 * Couvre les audits/revues des différents processus du SMQ (ISO 9001 §9.2).
 */

/* Processus / activité audité(e) */
export const PROCESSUS = [
  "Management",
  "Exploitation",
  "Développement",
  "Infrastructure",
  "Gestion des ressources",
  "Revue de direction",
];

export const STATUTS_AUDIT = ["Planifié", "Réalisé", "Reporté", "Annulé"];
export const STATUT_FILTER_OPTIONS = ["Tous les statuts", ...STATUTS_AUDIT];

/* Colonnes du tableau principal */
export const AUDITS_TABLE_COLUMNS = [
  "N° réf",
  "Processus audité",
  "Date planifiée",
  "Auditeur",
  "Périmètre / objectif",
  "Statut",
  "Date réalisée",
  "Écarts constatés",
  "Date clôture",
  "Prochain audit",
];

/* Mapping statut -> classes de couleur (badges) */
export const STATUT_STYLES = {
  "Planifié": "bg-blue-100 text-blue-700",
  "Réalisé": "bg-emerald-100 text-emerald-700",
  "Reporté": "bg-amber-100 text-amber-700",
  "Annulé": "bg-slate-100 text-slate-500",
};
