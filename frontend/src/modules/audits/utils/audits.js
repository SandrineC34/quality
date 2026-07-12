import { STATUT_STYLES } from "../constants/audits";
import { DEFAULT_BADGE_STYLE } from "../../dashboard/components/ui";

/** Classe de badge associée au statut d'un audit */
export function getAuditStatutClass(statut) {
  return STATUT_STYLES[statut] || DEFAULT_BADGE_STYLE;
}

/** Nouvel audit vide (formulaire de planification) */
export function emptyAudit() {
  return {
    processus: "",
    date_planifiee: new Date().toISOString().slice(0, 10),
    auditeur: "",
    perimetre: "",
    statut: "Planifié",
    date_realisation: "",
    constats: "",
    date_cloture: "",
    prochain_audit: "",
    rapport_reference: "",
  };
}
