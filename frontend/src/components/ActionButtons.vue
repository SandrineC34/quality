<template>
  <!-- Bouton ajouter-->
  <div class="flex items-center space-x-2">
    <button v-if="showAdd" @click="$emit('add')" :class="addClass">
      <slot name="add"><span>+ Ajouter</span></slot>
    </button>
    <!-- Bouton edit-->
    <button v-if="showEdit" @click="$emit('edit')" :class="editClass">
      <slot name="edit"><span>✎</span></slot>
    </button>
    <!--Bouton effacer-->
    <button v-if="showDelete" @click="$emit('delete')" :class="deleteClass">
      <slot name="delete"><span>🗑</span></slot>
    </button>
    <!--Enregistrer-->
    <!--Imprimer/Exporter-->
  </div>
</template>

<script setup>
defineProps({
  showAdd: { type: Boolean, default: false },
  showEdit: { type: Boolean, default: false },
  showDelete: { type: Boolean, default: false },
  addClass: { type: String, default: 'bg-[var(--opensilex-green)] hover:bg-[var(--primary-dark)] text-white px-2 py-1 rounded text-sm' },
  editClass: { type: String, default: 'bg-gray-300 text-xs px-1 rounded' },
  deleteClass: { type: String, default: 'bg-red-300 text-xs px-1 rounded' },
});
</script>
