import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../modules/dashboard/views/DashboardView.vue";
import NonConformitesView from "../modules/actions/views/NonConformitesView.vue";
import ModelesTableauxView from "../modules/dashboard/views/ModelesTableauxView.vue";
import IndicateursView from "../modules/indicators/views/IndicateursView.vue";
import SuiviActionsView from "../modules/actions/views/SuiviActionsView.vue";
import AuditsView from "../modules/audits/views/AuditsView.vue";
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/non-conformites" },
    { path: "/tableau-de-bord", name: "dashboard", component: DashboardView },
    { path: "/non-conformites", name: "non-conformites", component: NonConformitesView },
    { path: "/indicateurs", name: "indicateurs", component: IndicateursView },
    { path: "/actions", name: "actions", component: SuiviActionsView },
    { path: "/audits", name: "audits", component: AuditsView },
    { path: "/modeles", name: "modeles", component: ModelesTableauxView },
   
  ],
});

export default router;
