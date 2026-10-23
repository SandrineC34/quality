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
  <section class="section" id="matrice">
    <h2>Matrice SWOT</h2>

    <div class="swot-layout">

      <!-- Coin vide -->
      <div class="spacer"></div>

      <!-- En-têtes de colonnes -->
      <div class="header-positive">✓ Positif</div>
      <div class="header-negative">✗ Négatif</div>

      <!-- Label Interne -->
      <div class="label-box label-interne">Interne</div>

      <!-- Forces -->
      <SwotColumn
        title="Forces" tag="Interne" type="strength"
        :items="swotItems.filter(i => i.type === 'strength')"
        @add="addItem('strength')" @edit="editItem" @delete="deleteItem" />

      <!-- Faiblesses -->
      <SwotColumn
        title="Faiblesses" tag="Interne" type="weakness"
        :items="swotItems.filter(i => i.type === 'weakness')"
        @add="addItem('weakness')" @edit="editItem" @delete="deleteItem" />

      <!-- Label Externe -->
      <div class="label-box label-externe">Externe</div>

      <!-- Opportunités -->
      <SwotColumn
        title="Opportunités" tag="Externe" type="opportunity"
        :items="swotItems.filter(i => i.type === 'opportunity')"
        @add="addItem('opportunity')" @edit="editItem" @delete="deleteItem" />

      <!-- Menaces -->
      <SwotColumn
        title="Risques" tag="Externe" type="threat"
        :items="swotItems.filter(i => i.type === 'threat')"
        @add="addItem('threat')" @edit="editItem" @delete="deleteItem" />

    </div>
  </section>

  <!-- ══ PIED DE PAGE DOC ══ -->
  <section class="section">
    <div class="doc-footer">
      <span>OpenSILEX-SWOT</span> |
      <span contenteditable="true">Version 1.0</span> |
      <span contenteditable="true">Mise à jour : 21/04/2026 - Isabelle Alic</span>
    </div>
  </section>

  <!-- ══ EXPORT ══ -->
  <div class="export-bar">
    <button class="print-btn" @click="exportSwot">🖨 Imprimer / Exporter</button>
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
      console.warn('API not available – no data');
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
    console.warn('API unavailable – added item locally');
  }
}

async function editItem(item) {
  const newText = window.prompt('Modifier l\'élément', item.text);
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
    console.warn('API unavailable – deleted item locally');
  }
}

onMounted(fetchSwot);

function exportSwot() {
  const groupItems = (typeKey) => swotItems.value.filter(i => i.type === typeKey);

  const renderBox = (typeKey, title, tag) => {
    const items = groupItems(typeKey);
    const lis = items.map(i =>
      `<li><span class="swot-id">${i.ref ?? ''}</span><span>${i.text}</span></li>`
    ).join('');
    return `<div class="swot-box ${typeKey}s">
      <h3 class="box-title">${title} <span class="box-tag">${tag}</span></h3>
      <ul>${lis}</ul>
    </div>`;
  };

  const html = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Analyse SWOT - Export</title>
  <link rel="stylesheet" href="css/charte.css">
  <link rel="stylesheet" href="css/common.css">
  <link rel="stylesheet" href="css/processus/processus.css">
  <link rel="stylesheet" href="css/swot/swot.css">
</head>
<body class="modern-layout">
<header class="main-header"><div class="nav-container">
  <button class="print-btn-nav" onclick="window.print()">🖨 Imprimer</button>
</div></header>
<main class="modern-content swot-content">
  <section class="section" id="matrice">
    <h2>Matrice SWOT</h2>
    <div class="swot-layout">
      <div class="spacer"></div>
      <div class="header-positive">✓ Positif</div>
      <div class="header-negative">✗ Négatif</div>
      <div class="label-box label-interne">Interne</div>
      <div class="label-box label-externe">Externe</div>
      ${renderBox('strength',    'Forces',      'Interne')}
      ${renderBox('weakness',    'Faiblesses',  'Interne')}
      ${renderBox('opportunity', 'Opportunités','Externe')}
      ${renderBox('threat',      'Risques',     'Externe')}
    </div>
  </section>
</main>
</body>
</html>`;

  const blob = new Blob([html], { type: 'text/html' });
  const url  = URL.createObjectURL(blob);
  const win  = window.open(url, '_blank');
  if (win) win.onload = () => win.print();
  else console.warn('Popup blocked');
}
</script>

<style scoped>
/* ── Hero ── */
.proc-banner {
  background: linear-gradient(135deg, #1e3a5f 0%, #2d6a4f 100%);
  color: #fff;
  padding: 1.5rem 2rem;
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
.section { padding: 1.5rem 2rem; }
.section h2 {
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

:deep(.strengths)     { grid-column: 2; grid-row: 2; }
:deep(.weaknesses)    { grid-column: 3; grid-row: 2; }
:deep(.opportunities) { grid-column: 2; grid-row: 3; }
:deep(.threats)       { grid-column: 3; grid-row: 3; }

.header-positive,
.header-negative {
  text-align: center;
  font-weight: 700;
  font-size: 0.9rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
}
.header-positive { background: #dcfce7; color: #166534; }
.header-negative { background: #fee2e2; color: #991b1b; }

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