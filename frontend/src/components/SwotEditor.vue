<template>

  <!-- ══ HERO ══ -->
  <div class="proc-banner">
    <div class="proc-info">
      <div>
        <span class="proc-id-tag">OpenSILEX · Analyse stratégique</span>
        <h1>Analyse SWOT</h1>
        <div class="proc-hero-sub">
          <span class="h-sp1">Forces, Faiblesses, Opportunités &amp; Risques</span>
        </div>
      </div>
    </div>
  </div>

  <!-- ══ MATRICE ══ -->
  <section class="swot-section" id="matrice">
    <h2 class="swot-h2">Matrice SWOT</h2>

    <div class="swot-layout">

      <div class="spacer"></div>
      <div class="header-positive">✓ Positif</div>
      <div class="header-negative">✗ Négatif</div>

      <div class="label-box label-interne">Interne</div>

      <SwotColumn
        title="Forces" tag="Interne" type="strength"
        :items="swotItems.filter(i => i.type === 'strength')"
        @add="addItem('strength')" @edit="editItem" @delete="deleteItem" />

      <SwotColumn
        title="Faiblesses" tag="Interne" type="weakness"
        :items="swotItems.filter(i => i.type === 'weakness')"
        @add="addItem('weakness')" @edit="editItem" @delete="deleteItem" />

      <div class="label-box label-externe">Externe</div>

      <SwotColumn
        title="Opportunités" tag="Externe" type="opportunity"
        :items="swotItems.filter(i => i.type === 'opportunity')"
        @add="addItem('opportunity')" @edit="editItem" @delete="deleteItem" />

      <SwotColumn
        title="Risques" tag="Externe" type="threat"
        :items="swotItems.filter(i => i.type === 'threat')"
        @add="addItem('threat')" @edit="editItem" @delete="deleteItem" />

    </div>
  </section>

  <!-- ══ PIED DE PAGE DOC ══ -->
  <section class="swot-section">
    <div class="doc-footer">
      <span>OpenSILEX-SWOT</span> |
      <span contenteditable="true">Version 1.0</span> |
      <span contenteditable="true">Mise à jour : 21/04/2026 - Isabelle Alic</span>
    </div>
  </section>

  <!-- ══ EXPORT (masqué à l'impression) ══ -->
  <div class="export-bar">
    <button class="print-btn" @click="triggerPrint">🖨 Imprimer / Exporter PDF</button>
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import SwotColumn from './SwotColumn.vue';

const swotItems = ref([]);

async function fetchSwot() {
  try {
    const res = await fetch('/api/swot');
    if (!res.ok) throw new Error('Fetch failed');
    swotItems.value = await res.json();
    localStorage.setItem('swotData', JSON.stringify(swotItems.value));
  } catch (e) {
    const stored = localStorage.getItem('swotData');
    if (stored) {
      swotItems.value = JSON.parse(stored);
      console.warn('API unavailable – loaded SWOT data from localStorage');
    } else {
      swotItems.value = [];
    }
  }
}

async function addItem(type) {
  const text = window.prompt(`Nouvel élément (${type})`);
  if (!text) return;
  try {
    const res = await fetch('/api/swot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, text }),
    });
    if (!res.ok) throw new Error('Add failed');
    await fetchSwot();
  } catch (e) {
    const newId = Math.max(0, ...swotItems.value.map(i => i.id)) + 1;
    swotItems.value.push({ id: newId, type, text });
    localStorage.setItem('swotData', JSON.stringify(swotItems.value));
  }
}

async function editItem(item) {
  const newText = window.prompt("Modifier l'élément", item.text);
  if (newText === null) return;
  try {
    const res = await fetch(`/api/swot/${item.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: newText }),
    });
    if (!res.ok) throw new Error('Edit failed');
    const idx = swotItems.value.findIndex(i => i.id === item.id);
    if (idx !== -1) {
      swotItems.value[idx].text = newText;
      localStorage.setItem('swotData', JSON.stringify(swotItems.value));
    }
  } catch (e) {
    console.warn('API unavailable – edit not saved');
  }
}

async function deleteItem(item) {
  if (!window.confirm('Supprimer cet élément ?')) return;
  try {
    const res = await fetch(`/api/swot/${item.id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Delete failed');
    await fetchSwot();
  } catch (e) {
    swotItems.value = swotItems.value.filter(i => i.id !== item.id);
    localStorage.setItem('swotData', JSON.stringify(swotItems.value));
  }
}

function triggerPrint() {
  window.print();
}

onMounted(fetchSwot);
</script>

<!-- Style NON scoped : nécessaire pour que @media print atteigne
     les éléments des composants enfants (SwotColumn, ActionButtons) -->
<style>
@media print {
  @page { size: A4 portrait; margin: 8mm; }

  * {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  /* Masquer ce qui ne s'imprime pas */
  .export-bar,
  .main-header,
  .nav-footer,
  .menu-toggle {
    display: none !important;
  }

  /* Hero compact */
  .proc-banner {
    padding: 0.6rem 1rem !important;
  }
  .proc-banner h1 {
    font-size: 1.1rem !important;
    margin: 0.1rem 0 0 !important;
  }
  .proc-id-tag { font-size: 0.6rem !important; }
  .proc-hero-sub .h-sp1 { font-size: 0.7rem !important; }

  /* Section */
  .swot-section { padding: 0.4rem 0.6rem !important; margin-bottom: 0 !important; }
  .swot-h2 { font-size: 0.8rem !important; margin-bottom: 0.4rem !important; padding-bottom: 0.2rem !important; }

  /* Grille */
  .swot-layout { gap: 5px !important; }

  .header-positive,
  .header-negative {
    padding: 3px 6px !important;
    font-size: 0.6rem !important;
    background: inherit !important;
  }
  .header-positive { background: #dcfce7 !important; color: #166534 !important; }
  .header-negative { background: #fee2e2 !important; color: #991b1b !important; }

  .label-box {
    padding: 4px 2px !important;
    font-size: 0.58rem !important;
  }
  .label-interne { background: #d1fae5 !important; color: #065f46 !important; }
  .label-externe { background: #dbeafe !important; color: #1e40af !important; }

  /* Éviter les coupures de page dans la grille */
  .swot-layout,
  .swot-box { break-inside: avoid; page-break-inside: avoid; }

  /* Doc footer */
  .doc-footer { font-size: 0.6rem !important; }
}
</style>

<style scoped>
/* ── Hero ── */
.proc-banner {
  background: linear-gradient(135deg, #1e3a5f 0%, #2d6a4f 100%);
  color: #fff;
  padding: 1.5rem 2rem;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.proc-banner h1 { font-size: 1.6rem; margin: 0.25rem 0 0; }
.proc-id-tag {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .08em;
  opacity: .75;
}
.proc-hero-sub .h-sp1 { font-size: 0.95rem; opacity: .85; }

/* ── Section ── */
.swot-section { padding: 1.5rem 2rem; }
.swot-h2 {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1e3a5f;
  margin-bottom: 1.25rem;
  padding-bottom: 0.4rem;
  border-bottom: 2px solid #e5e7eb;
}

/* ══ GRILLE ══ */
.swot-layout {
  display: grid;
  grid-template-columns: 2.5rem 1fr 1fr;
  grid-template-rows: auto auto auto;
  gap: 0.75rem;
  align-items: stretch;
}

.spacer          { grid-column: 1; grid-row: 1; }
.header-positive { grid-column: 2; grid-row: 1; }
.header-negative { grid-column: 3; grid-row: 1; }
.label-interne   { grid-column: 1; grid-row: 2; }
.label-externe   { grid-column: 1; grid-row: 3; }

/* Placement des SwotColumn via :deep() */
:deep(.strengths)     { grid-column: 2; grid-row: 2; }
:deep(.weaknesses)    { grid-column: 3; grid-row: 2; }
:deep(.opportunities) { grid-column: 2; grid-row: 3; }
:deep(.threats)       { grid-column: 3; grid-row: 3; }

/* En-têtes */
.header-positive,
.header-negative {
  text-align: center;
  font-weight: 700;
  font-size: 0.9rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.header-positive { background: #dcfce7; color: #166534; }
.header-negative { background: #fee2e2; color: #991b1b; }

/* Labels verticaux */
.label-box {
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
  border-radius: 0.5rem;
  padding: 0.5rem 0.25rem;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.label-interne { background: #d1fae5; color: #065f46; }
.label-externe { background: #dbeafe; color: #1e40af; }

/* ── Pied de page doc ── */
.doc-footer {
  font-size: 0.8rem;
  color: #6b7280;
  border-top: 1px solid #e5e7eb;
  padding-top: 0.75rem;
}
.doc-footer span[contenteditable]:focus {
  outline: 1px dashed #9ca3af;
  border-radius: 2px;
}

/* ── Bouton export ── */
.export-bar { padding: 0.5rem 2rem 1.5rem; }
.print-btn {
  background: #1e3a5f;
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  padding: 0.45rem 1.1rem;
  font-size: 0.88rem;
  cursor: pointer;
  transition: background .15s;
}
.print-btn:hover { background: #2d6a4f; }
</style>