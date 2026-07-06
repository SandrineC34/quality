<script setup>
import { UI } from "../../constants/ui";

defineProps({
  titre: String,
  valeur: Number,
  couleur: {
    type: String,
    default: "text-slate-900",
  },
});
</script>

<template>
  <div :class="[UI.card, 'p-5']">
    <p class="text-xs font-medium text-slate-500 uppercase mb-2">
      {{ titre }}
    </p>
    <p class="text-2xl font-bold" :class="couleur">
      {{ valeur }}
    </p>
  </div>
</template>
