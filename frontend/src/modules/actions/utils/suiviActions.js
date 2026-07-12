import { STATUT_STYLES, EFFICACITE_STYLES } from "../constants/suiviActions";
import { DEFAULT_BADGE_STYLE } from "../../dashboard/components/ui";

/** Classe de badge associée au statut d'une action */
export function getActionSuiviStatutClass(statut) {
  return STATUT_STYLES[statut] || DEFAULT_BADGE_STYLE;
}

/** Classe de badge associée au résultat d'efficacité */
export function getEfficaciteClass(resultat) {
  return EFFICACITE_STYLES[resultat] || DEFAULT_BADGE_STYLE;
}

/**
 * Une action est en retard si sa date prévue est dépassée et qu'elle
 * n'est pas clôturée, indépendamment du statut saisi en base.
 */
export function isEnRetard(action) {
  if (!action || action.statut === "Clôturée" || !action.date_prevue) return false;
  const today = new Date(new Date().toDateString());
  return new Date(action.date_prevue) < today;
}

/** Statut affiché à l'écran : force "En retard" si la date prévue est dépassée */
export function displayStatut(action) {
  return isEnRetard(action) ? "En retard" : action.statut;
}

/** Nouvelle action de suivi vide */
export function emptySuiviAction() {
  return {
    date_creation: new Date().toISOString().slice(0, 10),
    origine: "",
    origine_ref: "",
    type_action: "",
    description: "",
    responsable: "",
    date_prevue: "",
    priorite: "",
    statut: "À faire",
    date_cloture: "",
    preuves: "",
    criteres_efficacite: "",
    date_mesure_efficacite: "",
    resultat_efficacite: "Non évaluée",
    commentaire_efficacite: "",
    valide_par: "",
  };
}
