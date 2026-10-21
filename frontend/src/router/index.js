import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../modules/dashboard/views/DashboardView.vue";
import NonConformitesView from "../modules/actions/views/NonConformitesView.vue";
import ModelesTableauxView from "../modules/dashboard/views/ModelesTableauxView.vue";
import ProcessusCartographieView from "../modules/Processus/views/CartographieView.vue";
import DocumentationView from "../modules/Documentations/views/DocumentationView.vue";
import PolitiqueView from "../modules/Pilotage et statégies/PolitiqueView.vue";
import SwotView from "../modules/Pilotage et statégies/SwotView.vue";
import TowsView from "../modules/Pilotage et statégies/TowsView.vue";
import PartieViews from "../modules/Pilotage et statégies/PartieView.vue";
import IndicateursView from "../modules/indicators/views/IndicateursView.vue";
import SuiviActionsView from "../modules/actions/views/SuiviActionsView.vue";
import AuditsView from "../modules/audits/views/AuditsView.vue";
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/non-conformites" },
    { path: "/tableau-de-bord", name: "dashboard", component: DashboardView },
    { path: "/pilotage/politique", name: "Statégie et Pilotage", component: PolitiqueView },
    { path: "/amelioration", name: "Amélioration continue", component: DashboardView },
    { path: "/audit", name: "Audits et évaluation", component: DashboardView },
    { path: "/non-conformites", name: "non-conformites", component: NonConformitesView },
    { path: "/indicateurs", name: "indicateurs", component: IndicateursView },
    { path: "/actions", name: "actions", component: SuiviActionsView },
    { path: "/audits", name: "audits", component: AuditsView },
    { path: "/modeles", name: "modeles", component: ModelesTableauxView },
    { path: "/politique", name: "politique", component: PolitiqueView },
    { path: "/pilotage/swot", name: "swot", component: SwotView },
    { path: "/pilotage/tows", name: "tows", component: TowsView },
    { path: "/pilotage/paries", name: "partie", component: PartieViews},   
    { path: "/processus/cartographie", name: "processus-cartographie", component: ProcessusCartographieView },
    { path: "/documentation", name: "documentation", component: DocumentationView },
   
  ],
});

export default router;
