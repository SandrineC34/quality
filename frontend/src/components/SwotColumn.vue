<template>
  <div class="swot-box" :class="boxClass">
    <h3 class="box-title">
      {{ title }}
      <span class="box-tag">{{ tag }}</span>
    </h3>

    <ul>
      <li v-for="item in items" :key="item.id">
        <span class="swot-id">{{ item.ref }}</span>
        <span v-html="item.text"></span>
        <span class="item-actions">
          <ActionButtons showEdit showDelete
            @edit="$emit('edit', item)"
            @delete="$emit('delete', item)" />
        </span>
      </li>
    </ul>

    <button class="btn-add" @click="$emit('add')" title="Ajouter un élément">＋ Ajouter</button>
  </div>
</template>

<script setup>
import ActionButtons from './ActionButtons.vue';

const props = defineProps({
  title: String,
  tag:   String,   // « Interne » ou « Externe »
  items: Array,
  type:  String,   // 'strength' | 'weakness' | 'opportunity' | 'threat'
});

const boxClassMap = {
  strength:    'strengths',
  weakness:    'weaknesses',
  opportunity: 'opportunities',
  threat:      'threats',
};
const boxClass = boxClassMap[props.type] ?? '';
</script>

<style scoped>
/* ── Box ── */
.swot-box {
  border-radius: 0.75rem;
  padding: 1.25rem 1.25rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Couleurs calquées sur swot.css */
.strengths     { background: #d1fae5; border: 2px solid #6ee7b7; }
.weaknesses    { background: #fee2e2; border: 2px solid #fca5a5; }
.opportunities { background: #dbeafe; border: 2px solid #93c5fd; }
.threats       { background: #fef9c3; border: 2px solid #fde047; }

/* ── Titre ── */
.box-title {
  font-size: 1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 0.5rem;
}

.box-tag {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(0,0,0,0.08);
  color: inherit;
  text-transform: uppercase;
  letter-spacing: .04em;
}

/* ── Liste ── */
ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.35rem; }

li {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  background: rgba(255,255,255,0.55);
  border-radius: 0.5rem;
  padding: 0.4rem 0.5rem;
  font-size: 0.88rem;
  line-height: 1.4;
}

li > span:nth-child(2) { flex: 1; }

/* ── Badge ref (S1, W2…) ── */
.swot-id {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 2rem;
  height: 1.35rem;
  border-radius: 4px;
  font-size: 0.72rem;
  font-weight: 700;
  color: #fff;
  padding: 0 4px;
}

.strengths     .swot-id { background: #059669; }
.weaknesses    .swot-id { background: #dc2626; }
.opportunities .swot-id { background: #2563eb; }
.threats       .swot-id { background: #ca8a04; }

/* ── Actions ── */
.item-actions {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

/* ── Bouton Ajouter ── */
.btn-add {
  margin-top: 0.25rem;
  align-self: flex-start;
  background: rgba(255,255,255,0.7);
  border: 1px dashed rgba(0,0,0,0.25);
  border-radius: 0.4rem;
  padding: 0.25rem 0.75rem;
  font-size: 0.8rem;
  cursor: pointer;
  color: #374151;
  transition: background .15s;
}
.btn-add:hover { background: rgba(255,255,255,0.95); }
</style>