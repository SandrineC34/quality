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

  <h1 class="titre"> MATRICE SWOT</h1>
  <div class="swot-editor">   
      
        <div class="swot-grid">
          <!-- En-têtes -->
          <div class="grid-corner"></div>
          <div class="grid-header header-positive">✓ Positif</div>
          <div class="grid-header header-negative">✗ Négatif</div>

          <!-- Ligne interne -->
          <div class="grid-label label-interne">Interne</div>

              <SwotColumn title="Forces"
                :items="swotItems.filter(i => i.type === 'strength')"
                @add="addItem('strength')" @edit="editItem" @delete="deleteItem" />

              <SwotColumn title="Faiblesses"
                :items="swotItems.filter(i => i.type === 'weakness')"
                @add="addItem('weakness')" @edit="editItem" @delete="deleteItem" />

              <!-- Ligne externe -->
              <div class="grid-label label-externe">Externe</div>

              <SwotColumn title="Opportunités"
                :items="swotItems.filter(i => i.type === 'opportunity')"
                @add="addItem('opportunity')" @edit="editItem" @delete="deleteItem" />
                
              <SwotColumn title="Menaces"
                :items="swotItems.filter(i => i.type === 'threat')"
                @add="addItem('threat')" @edit="editItem" @delete="deleteItem" />
        </div> 
        
       <!-- PIED DE PAGE DOC : version et date -->
          <section class="section">
            <div class="doc-footer">
              <span>OpenSILEX-SWOT</span> |
              <span contenteditable="true">Version 1.0</span> |
              <span contenteditable="true">Mise à jour : 21/04/2026 - Isabelle Alic</span>
              <!-- <span contenteditable="true">Mise à jour : 08/04/2026 - Anne Tireau</span> -->
              <!-- <span contenteditable="true">Mise à jour : 17/02/2026 - Sandrine Collavizza</span> -->
            </div>
          </section>

    <button @click="exportSwot" class="bg-gray-500 text-white px-3 py-1 rounded mt-4">Imprimer / Exporter</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import SwotColumn from './SwotColumn.vue';

const types = [
  { key: 'strength', title: 'Forces' },
  { key: 'weakness', title: 'Faiblesses' },
  { key: 'opportunity', title: 'Opportunités' },
  { key: 'threat', title: 'Menaces' },
];

const swotItems = ref([]);



async function fetchSwot() {
  try {
    const res = await fetch('/api/swot');
    if (!res.ok) throw new Error('Fetch failed');
    swotItems.value = await res.json();
    // Persist successful fetch in localStorage for offline fallback
    localStorage.setItem('swotData', JSON.stringify(swotItems.value));
  } catch (e) {
    // Try to load from localStorage before falling back to defaults
    const stored = localStorage.getItem('swotData');
    if (stored) {
      swotItems.value = JSON.parse(stored);
      console.warn('API unavailable – loaded SWOT data from localStorage');
    } else {
      console.warn('API not available – loading default SWOT data');
      swotItems.value = defaultSwot;
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
    // Fallback local update and persist to localStorage
    const newId = Math.max(...swotItems.value.map(i => i.id)) + 1;
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
    // Update locally only after successful API call
    const idx = swotItems.value.findIndex(i => i.id === item.id);
    if (idx !== -1) {
      swotItems.value[idx].text = newText;
      // Persist changes to localStorage for offline support
      localStorage.setItem('swotData', JSON.stringify(swotItems.value));
    }
  } catch (e) {
    // Do not modify locally if backend unavailable; just warn
    console.warn('API unavailable – edit not saved');
    // No local update, keep existing data (could also persist unchanged)
  }
}

async function deleteItem(item) {
  if (!window.confirm('Supprimer cet élément ?')) return;
  try {
    const res = await fetch(`/api/swot/${item.id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Delete failed');
    await fetchSwot();
  } catch (e) {
    // Fallback local deletion
      swotItems.value = swotItems.value.filter(i => i.id !== item.id);
      // Persist deletion to localStorage
      localStorage.setItem('swotData', JSON.stringify(swotItems.value));
      console.warn('API unavailable – deleted item locally');
  }
}

onMounted(fetchSwot);

function exportSwot() {
  // First generate HTML (same as before)
  const header = `<!DOCTYPE html>
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
<header class="main-header" id="header"><div class="nav-container"><button class="print-btn-nav" onclick="window.print()">🖨 Imprimer</button></div></header>
<main class="modern-content swot-content">
  <section class="section" id="matrice">
    <h2>Matrice SWOThgfhgf</h2>
    <div class="swot-layout">
      <div class="spacer"></div>
      <div class="header-positive">✓ Positif</div>
      <div class="header-negative">✗ Négatif</div>
      <div class="label-box label-interne">Interne</div>
      <div class="label-box label-externe">Externe</div>`;



  const footer = `</div></section></main></body></html>`;

  const groupItems = (typeKey) => swotItems.value.filter(i => i.type === typeKey);

  const renderBox = (typeKey, title, tag) => {
    const items = groupItems(typeKey);
    const lis = items.map(i => `<li><span class="swot-id">${i.ref}</span><span>${i.text}</span></li>`).join('');
    return `<div class="swot-box ${typeKey}s">
      <h3 class="box-title">${title} <span class="box-tag">${tag}</span></h3>
      <ul>${lis}</ul>
    </div>`;
  };

  const body = [
    renderBox('strength', 'Forces', 'Interne'),
    renderBox('weakness', 'Faiblesses', 'Interne'),
    renderBox('opportunity', 'Opportunités', 'Externe'),
    renderBox('threat', 'Risques', 'Externe'),
  ].join('');

  const html = header + body + footer;
  // Export SWOT HTML (same as before) for immediate preview/print
  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const win = window.open(url, '_blank');
  if (win) {
    win.onload = () => { win.print(); };
  } else {
    console.warn('Popup blocked – cannot open export window');
    }
  }
</script>

<style scoped>
.swot-editor { padding: 1rem; }

.swot-grid {
  display: grid;
  grid-template-columns: auto 1fr 1fr;
  gap: 1rem;
  align-items: stretch;
}

.grid-header,
.grid-label {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.grid-header {
  background: #f3f4f6;
  padding: 0.5rem;
  border-radius: 0.5rem;
}

.grid-label {
  /* étiquette verticale Interne/Externe */
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  background: #e5e7eb;
  padding: 0.5rem;
  border-radius: 0.5rem;
}

.header-positive { background: #dcfce7; color: #166534; }
.header-negative { background: #fee2e2; color: #991b1b; }

.titre { font-size: 1.25rem; color: red; }

.proc-banner { padding: 10px 0 12px; }
.proc-info h1 { font-size: 1.3rem; margin-bottom: 2px; }
.proc-id-tag { margin-bottom: 2px; }
</style>
