/**
 * Fonctions utilitaires génériques, utilisables par n'importe quelle page.
 */

/**
 * Formate une date ISO en date française lisible (JJ/MM/AAAA).
 * Retourne "-" si aucune valeur.
 */
export function formatDate(value) {
  if (!value) return "-";
  return new Date(value).toLocaleDateString("fr-FR");
}

/**
 * Transforme une erreur Axios/FastAPI en message lisible pour l'utilisateur.
 * Gère : erreurs de validation (tableau), détail texte, erreur serveur, erreur réseau.
 */
export function extractApiErrorMessage(err) {
  const detail = err?.response?.data?.detail;

  if (Array.isArray(detail)) {
    return detail.map((d) => `${d.loc?.at(-1)}: ${d.msg}`).join(" / ");
  }
  if (typeof detail === "string") {
    return detail;
  }
  if (err?.response) {
    return `Erreur serveur (${err.response.status}). Voir la console pour le détail.`;
  }
  return "Impossible de contacter le backend (réseau/CORS). Vérifiez qu'il tourne sur le port 8001.";
}

/**
 * Debounce générique : retarde l'exécution de `fn` de `delay` ms
 * et annule les appels précédents non exécutés.
 */
export function debounce(fn, delay = 300) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}
