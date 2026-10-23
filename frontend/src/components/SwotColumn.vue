<template>
  <div class="swot-box" :class="boxClass">
    <h3 class="box-title">
      {{ title }}
      <span class="box-tag">{{ tag }}</span>
    </h3>

    <ul>
      <li v-for="item in items" :key="item.id">
        <span class="swot-id">{{ item.ref }}</span>
        <span class="item-text" v-html="item.text"></span>
        <span class="item-actions">
          <ActionButtons showEdit showDelete
            @edit="$emit('edit', item)"
            @delete="$emit('delete', item)" />
        </span>
      </li>
    </ul>

    <button class="btn-add" @click="$emit('add')">＋ Ajouter</button>
  </div>
</template>

<script setup>
import ActionButtons from './ActionButtons.vue';

const props = defineProps({
  title: String,
  tag:   String,
  items: Array,
  type:  String,
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
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.strengths     { background: #d1fae5 !important; border: 2px solid #6ee7b7; }
.weaknesses    { background: #fee2e2 !important; border: 2px solid #fca5a5; }
.opportunities { background: #dbeafe !important; border: 2px solid #93c5fd; }
.threats       { background: #fef9c3 !important; border: 2px solid #fde047; }

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
  background: rgba(0,0,0,0.08) !important;
  color: inherit;
  text-transform: uppercase;
  letter-spacing: .04em;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

/* ── Liste ── */
ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.35rem; }

li {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  background: rgba(255,255,255,0.55) !important;
  border-radius: 0.5rem;
  padding: 0.4rem 0.5rem;
  font-size: 0.88rem;
  line-height: 1.4;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.item-text { flex: 1; }

/* ── Badge ref ── */
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
  color: #fff !important;
  padding: 0 4px;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.strengths     .swot-id { background: #059669 !important; }
.weaknesses    .swot-id { background: #dc2626 !important; }
.opportunities .swot-id { background: #2563eb !important; }
.threats       .swot-id { background: #ca8a04 !important; }

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

/* ── PRINT ── */
@media print {
  .btn-add,
  .item-actions { display: none !important; }

  .swot-box {
    border-radius: 0.5rem;
    padding: 0.6rem 0.75rem 0.5rem;
    gap: 0.2rem;
  }

  .strengths     { background: #d1fae5 !important; border: 2px solid #6ee7b7 !important; }
  .weaknesses    { background: #fee2e2 !important; border: 2px solid #fca5a5 !important; }
  .opportunities { background: #dbeafe !important; border: 2px solid #93c5fd !important; }
  .threats       { background: #fef9c3 !important; border: 2px solid #fde047 !important; }

  .box-title { font-size: 0.78rem; margin-bottom: 0.3rem; }
  .box-tag   { font-size: 0.58rem; padding: 1px 5px; }

  li {
    padding: 0.25rem 0.35rem;
    font-size: 0.65rem;
    gap: 0.35rem;
    background: rgba(255,255,255,0.55) !important;
  }

  .swot-id {
    font-size: 0.58rem;
    min-width: 1.6rem;
    height: 1.1rem;
  }

  .strengths     .swot-id { background: #059669 !important; color: #fff !important; }
  .weaknesses    .swot-id { background: #dc2626 !important; color: #fff !important; }
  .opportunities .swot-id { background: #2563eb !important; color: #fff !important; }
  .threats       .swot-id { background: #ca8a04 !important; color: #fff !important; }
}
</style>