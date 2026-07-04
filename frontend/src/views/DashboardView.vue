<script setup>
import { onMounted } from "vue";
import { useNonConformitesStore } from "../stores/nonConformites";

const store = useNonConformitesStore();
onMounted(() => store.fetchAll());
</script>

<template>
  <div>
    <p class="text-xs font-semibold text-red-600 uppercase tracking-wide mb-1">Registre qualité</p>
    <h1 class="text-3xl font-bold text-slate-900 mb-1">Tableau de bord</h1>
    <p class="text-slate-500 text-sm mb-6">Vue d'ensemble du système de management de la qualité</p>

    <div class="grid grid-cols-3 gap-4">
      <div class="bg-white rounded-xl border border-slate-200 p-5">
        <p class="text-xs font-medium text-slate-500 uppercase mb-2">Total NC</p>
        <p class="text-2xl font-bold text-slate-900">{{ store.items.length }}</p>
      </div>
      <div class="bg-white rounded-xl border border-slate-200 p-5">
        <p class="text-xs font-medium text-slate-500 uppercase mb-2">En cours</p>
        <p class="text-2xl font-bold text-blue-600">
          {{ store.items.filter((i) => i.statut === 'En cours').length }}
        </p>
      </div>
            <div class="bg-white rounded-xl border border-slate-200 p-5">
        <p class="text-xs font-medium text-slate-500 uppercase mb-2">Ouverte</p>
        <p class="text-2xl font-bold text-blue-600">
          {{ store.items.filter((i) => i.statut === 'En cours').length }}
        </p>
      </div>
      <div class="bg-white rounded-xl border border-slate-200 p-5">
        <p class="text-xs font-medium text-slate-500 uppercase mb-2">Clôturées</p>
        <p class="text-2xl font-bold text-emerald-600">
          {{ store.items.filter((i) => i.statut === 'Clôturée').length }}
        </p>
      </div>
    </div>
  </div>
</template>
