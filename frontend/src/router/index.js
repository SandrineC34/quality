import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../views/DashboardView.vue";
import NonConformitesView from "../views/NonConformitesView.vue";
import ModelesTableauxView from "../views/ModelesTableauxView.vue";


const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/non-conformites" },
    { path: "/tableau-de-bord", name: "dashboard", component: DashboardView },
    { path: "/non-conformites", name: "non-conformites", component: NonConformitesView },
    { path: "/modeles", name: "modeles", component: ModelesTableauxView },
   
  ],
});

export default router;
