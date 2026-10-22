<template>
  <div class="tows-editor">
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
    <button @click="exportTows" class="bg-gray-500 text-white px-3 py-1 rounded mt-4">Export TOWS</button>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  swotItems: {
    type: Array,
    required: true,
  },
});

function exportTows() {
  const towsHeader = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Analyse TOWS - Export</title>
  <link rel="stylesheet" href="/css/charte.css">
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

  const renderTowsBox = (typeKey, title, tag, extraClass) => {
    const items = props.swotItems.filter(i => i.type === typeKey);
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

  // Send to backend for writing (optional – kept from original)
  fetch('/api/swot/tows', {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain' },
    body: towsHtml,
  })
    .then(res => {
      if (!res.ok) throw new Error('Failed to save TOWS');
      const win = window.open('/Enjeux/2-tows.html', '_blank');
      if (win) { win.onload = () => { win.print(); }; }
    })
    .catch(e => console.error('TOWS export error:', e));
}
</script>

<style scoped>
.tows-editor { padding: 1rem; }
</style>
