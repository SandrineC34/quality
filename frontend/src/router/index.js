import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../modules/dashboard/views/DashboardView.vue";
import NonConformitesView from "../modules/actions/views/NonConformitesView.vue";
import ModelesTableauxView from "../modules/dashboard/views/ModelesTableauxView.vue";
import ProcessusCartographieView from "../modules/Processus/views/CartographieView.vue";
import DocumentationView from "../modules/Documentations/views/DocumentationView.vue";
import PolitiqueView from "../modules/politique/views/PolitiqueView.vue";
import SwotView from "../modules/enjeux/views/SwotView.vue";
import TowsView from "../modules/enjeux/views/TowsView.vue";
import IndicateursView from "../modules/indicators/views/IndicateursView.vue";
import SuiviActionsView from "../modules/actions/views/SuiviActionsView.vue";
import AuditsView from "../modules/audits/views/AuditsView.vue";
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/non-conformites" },
    { path: "/tableau-de-bord", name: "dashboard", component: DashboardView },
    { path: "/pilotage", name: "Statégie et Pilotage", component: DashboardView },
    { path: "/amelioration", name: "Amélioration continue", component: DashboardView },
    { path: "/audit", name: "Audits et évaluation", component: DashboardView },
    { path: "/non-conformites", name: "non-conformites", component: NonConformitesView },
    { path: "/indicateurs", name: "indicateurs", component: IndicateursView },
    { path: "/actions", name: "actions", component: SuiviActionsView },
    { path: "/audits", name: "audits", component: AuditsView },
    { path: "/modeles", name: "modeles", component: ModelesTableauxView },
    { path: "/politique", name: "politique", component: PolitiqueView },
    { path: "/enjeux/swot", name: "swot", component: SwotView },
    { path: "/enjeux/tows", name: "tows", component: TowsView },   
    { path: "/processus/cartographie", name: "processus-cartographie", component: ProcessusCartographieView },
    { path: "/documentation", name: "documentation", component: DocumentationView },
   
  ],
});

export default router;
