<script setup>
import { LayoutGrid, ShieldAlert, Table2, Shield, LineChart, ListChecks, ClipboardList } from "lucide-vue-next";

const navItems = [
  { to: "/tableau-de-bord", label: "Tableau de bord", icon: LayoutGrid },
  { to: "/indicateurs", label: "Indicateurs qualité", icon: LineChart },
  { to: "/non-conformites", label: "Non-conformités", icon: ShieldAlert },
  { to: "/actions", label: "Suivi des actions", icon: ListChecks },
  { to: "/audits", label: "Audits internes", icon: ClipboardList },
  { to: "/modeles", label: "Modèles de tableaux", icon: Table2 },
];
</script>

<template>
  <aside class="w-64 min-h-screen bg-slate-900 text-slate-200 flex flex-col shrink-0">
    <div class="flex items-center gap-3 px-5 py-6">
      <div class="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center">
        <Shield class="w-5 h-5 text-white" />
      </div>
      <div>
        <p class="text-sm font-semibold text-white leading-tight">SMQ Qualité</p>
        <p class="text-xs text-slate-400 leading-tight">ISO 9001</p>
      </div>
    </div>

    <p class="px-5 text-xs font-semibold text-slate-500 uppercase tracking-wide mt-2 mb-2">
      Navigation
    </p>

    <nav class="flex flex-col gap-1 px-3">
      <router-link
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
        :class="
          $route.path === item.to
            ? 'bg-blue-600 text-white'
            : 'text-slate-300 hover:bg-slate-800 hover:text-white'
        "
      >
        <component :is="item.icon" class="w-4 h-4" />
        {{ item.label }}
      </router-link>
    </nav>
  </aside>
</template>
