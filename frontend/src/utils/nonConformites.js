import {
  STATUT_STYLES,
  ACTION_STATUT_STYLES,
} from "../constants/nonConformites";
import { DEFAULT_BADGE_STYLE } from "../constants/ui";

/** Classe de badge associée au statut d'une non-conformité */
export function getStatutClass(statut) {
  return STATUT_STYLES[statut] || DEFAULT_BADGE_STYLE;
}

/** Classe de badge associée au statut d'une action corrective */
export function getActionStatutClass(statut) {
  return ACTION_STATUT_STYLES[statut] || DEFAULT_BADGE_STYLE;
}

/** Nouvelle action corrective vide */
export function emptyAction() {
  return { description: "", pilote: "", date_objectif: "", date_cloture: "", preuve: "", statut: "À faire" };
}

/** Nouveau formulaire de non-conformité vide */
export function emptyNCForm() {
  return {
    date : new Date().toISOString().slice(0, 10),
    source: "Audit interne",
    service_impacte: "Management",  
    description: "",
    gravite: "Majeure",
    statut: "En cours",
    analyse_causes: "",
    actions_correctives: [],
    date_cloture: "",
    
  };
}
