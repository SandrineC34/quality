<script setup>
import { onMounted } from "vue";
import { useNonConformitesStore } from "../stores/nonConformites";
import StatCard from "../components/ncs/NCStatCard.vue";

const store = useNonConformitesStore();

onMounted(() => {
  store.fetchAll();
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
          :valeur="store.items.length"
        />

        <StatCard
          titre="À faire"
          :valeur="store.items.filter(i => i.statut === 'A faire').length"
          couleur="text-orange-500"
        />

        <StatCard
          titre="Clôturées"
          :valeur="store.items.filter(i => i.statut === 'Clôturée').length"
          couleur="text-emerald-600"
        />

      </div>

    </section>

  </div>
</template>