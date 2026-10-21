<template>
  <div class="swot-editor">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <SwotColumn
        v-for="type in types"
        :key="type.key"
        :title="type.title"
        :items="swotItems.filter(i => i.type === type.key)"
        @add="addItem(type.key)"
        @edit="editItem"
        @delete="deleteItem"
      />
    </div>
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
  } catch (e) {
    console.warn('API unavailable – could not fetch SWOT data');
    swotItems.value = [];
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
    console.warn('API unavailable – could not add item');
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
    console.warn('API unavailable – could not delete item');
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
  <link rel="stylesheet" href="../../css/charte.css">
  <link rel="stylesheet" href="../../css/common.css">
  <link rel="stylesheet" href="../../css/processus/processus.css">
  <link rel="stylesheet" href="../../css/swot/swot.css">
</head>
<body class="modern-layout">
<header class="main-header" id="header"><div class="nav-container"><button class="print-btn-nav" onclick="window.print()">🖨 Imprimer</button></div></header>
<main class="modern-content swot-content">
  <section class="section" id="matrice">
    <h2>Matrice SWOT</h2>
    <div class="swot-layout">
`






  const footer = `</div></section></main></body></html>`;

  const groupItems = (typeKey) => swotItems.value.filter(i => i.type === typeKey);

  const renderBox = (typeKey, title, tag) => {
    const items = groupItems(typeKey);
    const lis = items.map(i => `<li><span class="swot-id">${i.id}</span><span>${i.text}</span></li>`).join('');
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

  // ---- Generate TOWS HTML and save to backend ----
  const towsHeader = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Analyse TOWS - Export</title>
  <link rel="stylesheet" href="../../css/charte.css">
  <link rel="stylesheet" href="../../css/common.css">
  <link rel="stylesheet" href="../../css/processus/processus.css">
  <link rel="stylesheet" href="../../css/swot/twos.css">
</head>
<body class="modern-layout">
<header class="main-header" id="header"><div class="nav-container"><button class="print-btn-nav" onclick="window.print()">🖨 Imprimer</button></div></header>
<main class="modern-content tows-content">
  <section class="section" id="matrice">
    <h2>Matrice TOWS</h2>
    <div class="tows-grid">
      <div class="spacer" aria-hidden="true"></div>
`; // Simplified grid start

  const towsFooter = `</div></section></main></body></html>`;

  // Reuse same groups for TOWS sections
  const renderTowsBox = (typeKey, title, tag, extraClass) => {
    const items = swotItems.value.filter(i => i.type === typeKey);
    const lis = items.map(i => `<li><span class="swot-id">${i.id}</span><span>${i.text}</span></li>`).join('');
    return `<div class="factor-card f-${extraClass}">
      <h3 class="box-title">${title} <span class="box-tag">${tag}</span></h3>
      <ul>${lis}</ul>
    </div>`;
  };

  const towsBody = [
    renderTowsBox('opportunity', 'Opportunités', 'Externe', 'o'),
    renderTowsBox('threat', 'Risques', 'Externe', 't'),
    renderTowsBox('strength', 'Forces', 'Interne', 's'),
    renderTowsBox('weakness', 'Faiblesses', 'Interne', 'w'),
  ].join('');

  const towsHtml = towsHeader + towsBody + towsFooter;

  // Send to backend for writing
  fetch('/api/swot/tows', {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain' },
    body: towsHtml,
  }).then(res => {
    if (!res.ok) throw new Error('Failed to save TOWS');
    // Open the saved file for printing
    const winT = window.open('/Enjeux/2-tows.html', '_blank');
    if (winT) { winT.onload = () => { winT.print(); }; }
  }).catch(e => console.error('TOWS export error:', e));
}
</script>

<style scoped>
.swot-editor { padding: 1rem; }
</style>
