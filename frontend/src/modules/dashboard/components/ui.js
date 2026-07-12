/**
 * Classes Tailwind génériques, indépendantes de tout module métier.
 * Utilisées par n'importe quelle page (Non-conformités, Indicateurs, ...).
 */
export const UI = {
  card: "bg-white rounded-xl border border-slate-200",

  label: "block text-sm font-medium text-slate-700 mb-1",
  labelSm: "block text-xs font-medium text-slate-500 mb-1",

  input:
    "w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
  textarea:
    "w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y",
  select:
    "w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500",

  btnPrimary:
    "px-4 py-2 rounded-lg bg-slate-900 text-sm font-medium text-white hover:bg-slate-800",
  btnSecondary:
    "px-4 py-2 rounded-lg border border-slate-300 text-sm font-medium text-slate-700 hover:bg-slate-50",

  badge: "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",

  pageEyebrow: "text-xs font-semibold text-red-600 uppercase tracking-wide mb-1",
  pageTitle: "text-3xl font-bold text-slate-900",
  pageSubtitle: "text-slate-500 text-sm mb-6",
};

/** Classe de badge par défaut quand un statut ne correspond à aucun mapping connu */
export const DEFAULT_BADGE_STYLE = "bg-slate-100 text-slate-700";

/** Délai de debounce par défaut pour les champs de recherche (ms) */
export const SEARCH_DEBOUNCE_MS = 300;