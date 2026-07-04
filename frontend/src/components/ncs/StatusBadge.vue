<script setup>
defineProps({
  statut: { type: String, required: true },
});

const styles = {
  Ouverte: "bg-orange-100 text-orange-700",
  "En cours": "bg-blue-100 text-blue-700",
  Clôturée: "bg-emerald-100 text-emerald-700",
};
</script>

<template>
  <span
    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
    :class="styles[statut] || 'bg-slate-100 text-slate-700'"
  >
    {{ statut }}
  </span>
</template>
