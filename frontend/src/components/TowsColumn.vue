<template>
  <div class="border rounded p-2">
    <div class="flex justify-between items-center mb-2">
      <h3 class="font-bold">{{ title }}</h3>
      <ActionButtons showAdd @add="$emit('add')" />
    </div>
    <ul>
      <li v-for="item in items" :key="item.id" class="flex justify-between items-center mb-1">
        <span class="flex-1" v-html="item.text"></span>
        <ActionButtons showEdit showDelete @edit="$emit('edit', item)" @delete="$emit('delete', item)" />
      </li>
    </ul>
  </div>
</template>

<script setup>
import ActionButtons from './ActionButtons.vue';

defineProps({
  title: String,
  items: Array,
});
</script>

<style scoped>
ul { list-style: none; padding: 0; margin: 0; }
li { background: #f9f9f9; padding: 4px 6px; border-radius: 4px; }
</style>