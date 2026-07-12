<script setup>
import { onMounted, computed } from "vue";
import { useNonConformitesStore } from "../../actions/stores/nonConformites.js";
import StatCard from "../../actions/components/ncs/NCStatCard.vue";

const store = useNonConformitesStore();

onMounted(() => {
  store.fetchAll();
});

const totalActions = computed(() => {
  return store.items.reduce((acc, item) => acc + (item.actions_correctives || []).length, 0);
});

const actionsAFaire = computed(() => {
  return store.items.reduce((acc, item) => acc + (item.actions_correctives || []).filter(a => a.statut === "À faire").length, 0);
});

const actionsCloturees = computed(() => {
  return store.items.reduce((acc, item) => acc + (item.actions_correctives || []).filter(a => a.statut === "Clôturée" || a.date_cloture).length, 0);
});
</script>

<template>
  <div>

    <p class="text-xs font-semibold text-red-600 uppercase tracking-wide mb-1">
      Registre qualité
    </p>

    <h1 class="text-3xl font-bold text-slate-900 mb-1">
      Tableau de bord
    </h1>

    <p class="text-slate-500 text-sm mb-8">
      Vue d'ensemble du système de management de la qualité
    </p>

    <!-- ========================= -->
    <!-- NON CONFORMITES -->
    <!-- ========================= -->

    <section class="mb-10">

      <h2 class="text-2xl font-bold text-slate-900 mb-4">
        Statuts des non-conformités
      </h2>

      <div class="grid grid-cols-4 gap-4">

        <StatCard
          titre="Total NC"
          :valeur="store.items.length"
        />

        <StatCard
          titre="En cours"
          :valeur="store.items.filter(i => i.statut === 'En cours').length"
          couleur="text-blue-600"
        />

        <StatCard
          titre="Ouvertes"
          :valeur="store.items.filter(i => i.statut === 'Ouverte').length"
          couleur="text-orange-500"
        />

        <StatCard
          titre="Clôturées"
          :valeur="store.items.filter(i => i.statut === 'Clôturée').length"
          couleur="text-emerald-600"
        />

      </div>

    </section>

    <!-- ========================= -->
    <!-- ACTIONS -->
    <!-- ========================= -->

    <section>

      <h2 class="text-2xl font-bold text-slate-900 mb-4">
        Statuts des actions
      </h2>

      <div class="grid grid-cols-3 gap-4">

        <StatCard
          titre="Total"
          :valeur="totalActions"
        />

        <StatCard
          titre="À faire"
          :valeur="actionsAFaire"
          couleur="text-orange-500"
        />

        <StatCard
          titre="Clôturées"
          :valeur="actionsCloturees"
          couleur="text-emerald-600"
        />

      </div>

    </section>

  </div>
</template>