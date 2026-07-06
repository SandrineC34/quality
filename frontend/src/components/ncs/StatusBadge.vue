<script setup>
import { UI } from "../../constants/ui";
import { getStatutClass } from "../../utils/nonConformites";

defineProps({
  statut: { type: String, required: true },
});
</script>

<template>
  <span :class="[UI.badge, getStatutClass(statut)]">
    {{ statut }}
  </span>
</template>
