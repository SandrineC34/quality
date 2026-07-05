<script setup>
defineProps({
  titre: String,
  valeur: Number,
  couleur: {
    type: String,
    default: "text-slate-900"
  }
});
</script>

<template>
  <div class="bg-white rounded-xl border border-slate-200 p-5">
    <p class="text-xs font-medium text-slate-500 uppercase mb-2">
      {{ titre }}
    </p>
    <p class="text-2xl font-bold" :class="couleur">
      {{ valeur }}
    </p>
  </div>
</template>