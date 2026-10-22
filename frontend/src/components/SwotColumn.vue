<template>
  <div class="border rounded p-2">
    <div class="flex justify-between items-center mb-2">
      <!--<h3 class="font-bold">{{ title }}</h3>-->
      <h3 class="title-colonn">{{ title }}</h3>
      <ActionButtons showAdd @add="$emit('add')" />
    </div>
    <ul>
        <li v-for="item in items" :key="item.id" class="flex justify-between items-center mb-1">          
          <span class="badge mr-2" :class="badgeClass(item.type)">{{ item.ref }}</span>
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

function badgeClass(type) {
  const map = {
    'strength': 'badge-force',
    'weakness': 'badge-faiblesse',
    'opportunity': 'badge-opportunite',
    'threat': 'badge-risque',
    // fallback for legacy titles
    'Force': 'badge-force',
    'Faiblesse': 'badge-faiblesse',
    'Opportunité': 'badge-opportunite',
    'Risque': 'badge-risque',
  };
  return map[type] || 'badge-force';
}

</script>

<style scoped>

.title-colonn { font-size: 1.5em; font-style: bold;} 

ul { list-style: none; padding: 0; margin: 0; }
li { background: #f9f9f9; padding: 4px 6px; border-radius: 4px; }

.badge {
  display: inline-block;
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.75em;
  font-weight: bold;
  color: #fff;
  flex-shrink: 0;
  }
/* 🟢 Force */
.badge-force { background: #2ecc71; color: #fff; }
/* 🟠 Faiblesse */
.badge-faiblesse { background: #f39c12; color: #fff; }
/* 🔵 Opportunité */
.badge-opportunite { background: #3498db; color: #fff; }
/* 🔴 Risque */
.badge-risque { background: #e74c3c; color: #fff; }

</style>
