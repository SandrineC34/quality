import { STATUT_STYLES, PERIOD_LABELS } from "../constants/indicateurs";
import { DEFAULT_BADGE_STYLE } from "../../dashboard/components/ui";

/** Classe de badge associée au statut d'un indicateur */
export function getStatutClass(statut) {
  return STATUT_STYLES[statut] || DEFAULT_BADGE_STYLE;
}

/** Libellés des champs de relevé attendus pour une fréquence donnée */
export function getPeriodeLabels(frequence) {
  return PERIOD_LABELS[frequence] || PERIOD_LABELS.Mensuelle;
}

/** Nouveau formulaire d'indicateur vide */
export function emptyIndicateurForm() {
  return {
    processus: "",
    reference_interne: "",
    reference_iso: "",
    description: "",
    unite: "",
    cible: null,
    sens_cible: "Plus est mieux",
    frequence: "Mensuelle",
    methode_calcul: "Moyenne",
    valeurs: new Array(getPeriodeLabels("Mensuelle").length).fill(null),
    responsable: "",
    commentaires: "",
  };
}

/**
 * Adapte le tableau de relevés à la longueur attendue par la fréquence choisie,
 * en conservant les valeurs déjà saisies (utile quand l'utilisateur change la fréquence).
 */
export function resizeValeurs(valeurs, frequence) {
  const size = getPeriodeLabels(frequence).length;
  const next = new Array(size).fill(null);
  for (let i = 0; i < Math.min(size, (valeurs || []).length); i++) {
    next[i] = valeurs[i];
  }
  return next;
}

/** Calcule le résultat annuel à partir des relevés saisis et de la méthode d'agrégation */
export function computeResultatAnnuel(valeurs, methode) {
  const saisies = (valeurs || []).filter((v) => v !== null && v !== "" && !Number.isNaN(Number(v)));
  if (saisies.length === 0) return null;
  const nombres = saisies.map(Number);

  if (methode === "Somme") {
    return arrondi(nombres.reduce((acc, v) => acc + v, 0));
  }
  if (methode === "Dernière valeur") {
    return arrondi(nombres[nombres.length - 1]);
  }
  // Moyenne par défaut
  return arrondi(nombres.reduce((acc, v) => acc + v, 0) / nombres.length);
}

/** Écart entre le résultat annuel et la cible. Positif = favorable, quel que soit le sens souhaité. */
export function computeEcart(resultat, cible, sensCible) {
  if (resultat === null || cible === null || cible === undefined || Number.isNaN(cible)) return null;
  return arrondi(sensCible === "Moins est mieux" ? cible - resultat : resultat - cible);
}

/**
 * Détermine le statut de performance à partir de l'écart et de la cible.
 * Règle retenue : atteint si l'écart est favorable ou nul ; à surveiller si
 * l'écart défavorable reste dans une tolérance de 10 % de la cible ; non atteint au-delà.
 * (Seuil de tolérance ajustable selon les besoins de l'organisation.)
 */
export function computeStatut(ecart, cible) {
  if (ecart === null) return null;
  if (ecart >= 0) return "Atteint";
  const tolerance = Math.abs(cible) * 0.1 || 1;
  return Math.abs(ecart) <= tolerance ? "À surveiller" : "Non atteint";
}

function arrondi(nombre) {
  return Math.round(nombre * 100) / 100;
}
