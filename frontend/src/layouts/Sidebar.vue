<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import {
  Shield,
  LayoutDashboard,
  CheckSquare,
  Compass,
  Workflow,
  FileText,
  RefreshCcw,
  ClipboardCheck,
  Users,
  Factory,
  Settings,
  ChevronDown,
} from "lucide-vue-next";

/*
  Structure de navigation (alignée sur les chapitres ISO 9001).
  - Un item avec `to`       : lien direct
  - Un item avec `children` : groupe repliable
*/
const navItems = [
  { to: "/tableau-de-bord", label: "Tableau de bord", icon: LayoutDashboard },
  { to: "/mes-taches", label: "Mes tâches", icon: CheckSquare },

  {
    label: "Pilotage et stratégie",
    icon: Compass,
    children: [
      { to: "/pilotage/contexte", label: "Contexte de l'organisme" },
      { to: "/pilotage/swot", label: "Analyse SWOT" },
      { to: "/pilotage/tows", label: "Analyse TOWS" },
      { to: "/pilotage/politique", label: "Politique qualité" },
      { to: "/pilotage/objectifs", label: "Objectifs qualité" },
      { to: "/pilotage/roles", label: "Rôles et responsabilités" },
      { to: "/pilotage/risques", label: "Risques et opportunités" },
    ],
  },

  {
    label: "Processus",
    icon: Workflow,
    children: [
      { to: "/processus/cartographie", label: "Cartographie" },
      { to: "/processus/fiches", label: "Cartes d'identité" },
      { to: "/processus/indicateurs", label: "Indicateurs par processus" },
    ],
  },

  {
    label: "Documentation",
    icon: FileText,
    children: [
      { to: "/documentation/base", label: "Base documentaire" },
      { to: "/documentation/a-reviser", label: "Documents à réviser" },
      { to: "/documentation/modeles", label: "Modèles de tableaux" },
    ],
  },

  {
    label: "Amélioration continue",
    icon: RefreshCcw,
    children: [
      { to: "/amelioration/non-conformites", label: "Non-conformités" },
      { to: "/amelioration/actions", label: "Actions correctives" },
      { to: "/amelioration/reclamations", label: "Réclamations clients" },
      { to: "/amelioration/plan-actions", label: "Plan d'actions global" },
    ],
  },

  {
    label: "Audits et évaluation",
    icon: ClipboardCheck,
    children: [
      { to: "/audits/programme", label: "Programme d'audits" },
      { to: "/audits/rapports", label: "Rapports et constats" },
      { to: "/audits/revue-direction", label: "Revue de direction" },
      { to: "/audits/satisfaction", label: "Satisfaction client" },
    ],
  },

  {
    label: "Ressources",
    icon: Users,
    children: [
      { to: "/ressources/competences", label: "Compétences et formations" },
      { to: "/ressources/polyvalence", label: "Matrice de polyvalence" },
      { to: "/ressources/equipements", label: "Équipements et métrologie" },
      { to: "/ressources/fournisseurs", label: "Fournisseurs" },
    ],
  },

  { to: "/realisation", label: "Réalisation", icon: Factory },

  {
    label: "Administration",
    icon: Settings,
    children: [
      { to: "/administration/utilisateurs", label: "Utilisateurs et droits" },
      { to: "/administration/parametrage", label: "Paramétrage" },
      { to: "/administration/historique", label: "Journal d'historique" },
    ],
  },
];

const route = useRoute();

const isActive = (to) => route.path === to || route.path.startsWith(to + "/");
const hasActiveChild = (item) => item.children?.some((c) => isActive(c.to));

// Groupes ouverts : celui de la page courante s'ouvre automatiquement
const openGroups = ref(new Set());

watch(
  () => route.path,
  () => {
    navItems.forEach((item) => {
      if (item.children && hasActiveChild(item)) openGroups.value.add(item.label);
    });
  },
  { immediate: true }
);

const isOpen = (label) => openGroups.value.has(label);

function toggle(label) {
  const next = new Set(openGroups.value);
  next.has(label) ? next.delete(label) : next.add(label);
  openGroups.value = next;
}
</script>

<template>
  <aside class="w-64 min-h-screen flex flex-col shrink-0 bg-[var(--nav-bg)] text-[var(--nav-text)]">
    <!-- Logo -->
    <div class="flex items-center gap-3 px-5 py-6">
      <div class="w-9 h-9 rounded-lg flex items-center justify-center bg-[var(--nav-logo-bg)]">
        <Shield class="w-5 h-5 text-[var(--nav-logo-icon)]" />
      </div>
      <div>
        <p class="text-sm font-semibold leading-tight text-[var(--nav-text-strong)]">SMQ Qualité</p>
        <p class="text-xs leading-tight text-[var(--nav-text-muted)]">ISO 9001</p>
      </div>
    </div>

    <p class="px-5 mt-2 mb-2 text-xs font-semibold tracking-wide text-[var(--nav-section-title)]">
      Navigation
    </p>

    <nav class="flex flex-col gap-1 px-3 pb-6 overflow-y-auto" aria-label="Navigation principale">
      <div v-for="item in navItems" :key="item.label">
        <!-- Groupe repliable -->
        <template v-if="item.children">
          <button
            type="button"
            class="nav-focus w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-left transition-colors hover:bg-[var(--nav-hover-bg)] hover:text-[var(--nav-hover-text)]"
            :class="hasActiveChild(item) ? 'text-[var(--nav-group-active-text)]' : 'text-[var(--nav-text)]'"
            :aria-expanded="isOpen(item.label)"
            @click="toggle(item.label)"
          >
            <component :is="item.icon" class="w-4 h-4 shrink-0" />
            <span class="flex-1">{{ item.label }}</span>
            <ChevronDown
              class="w-4 h-4 shrink-0 text-[var(--nav-text-muted)] transition-transform"
              :class="{ 'rotate-180': isOpen(item.label) }"
            />
          </button>

          <div
            v-show="isOpen(item.label)"
            class="ml-5 mt-1 mb-1 pl-3 flex flex-col gap-0.5 border-l border-[var(--nav-border)]"
          >
            <router-link
              v-for="child in item.children"
              :key="child.to"
              :to="child.to"
              class="nav-focus px-3 py-2 rounded-lg text-sm transition-colors"
              :class="
                isActive(child.to)
                  ? 'bg-[var(--nav-active-bg)] text-[var(--nav-active-text)] font-medium'
                  : 'text-[var(--nav-text)] hover:bg-[var(--nav-hover-bg)] hover:text-[var(--nav-hover-text)]'
              "
            >
              {{ child.label }}
            </router-link>
          </div>
        </template>

        <!-- Lien direct -->
        <router-link
          v-else
          :to="item.to"
          class="nav-focus flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="
            isActive(item.to)
              ? 'bg-[var(--nav-active-bg)] text-[var(--nav-active-text)]'
              : 'text-[var(--nav-text)] hover:bg-[var(--nav-hover-bg)] hover:text-[var(--nav-hover-text)]'
          "
        >
          <component :is="item.icon" class="w-4 h-4 shrink-0" />
          {{ item.label }}
        </router-link>
      </div>
    </nav>
  </aside>
</template>

<style scoped>
.nav-focus:focus-visible {
  outline: 2px solid var(--nav-focus-ring);
  outline-offset: 2px;
}
</style>