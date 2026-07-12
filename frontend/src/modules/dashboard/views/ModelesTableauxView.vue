<script setup>
import { UI } from "../components/ui";
</script>

<template>
  <div>
    <p :class="UI.pageEyebrow">Registre qualité</p>
    <h1 :class="[UI.pageTitle, 'mb-1']">Modèles de tableaux</h1>
    <p :class="UI.pageSubtitle">Modèles réutilisables pour vos registres (à venir).</p>
    <div :class="[UI.card, 'p-10 text-center text-slate-400']">
      Aucun modèle pour l'instant.
    </div>
  </div>
</template>
