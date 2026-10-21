function printCompact() {
  // Exemple simple pour ajuster les styles lors de l'impression
  const style = document.createElement('style');
  style.type = 'text/css';
  style.media = 'print';
  style.appendChild(document.createTextNode(`
    @page {
      margin: 10mm; /* marges réduites */
      size: A4;
    }
    body {
      font-size: 10pt; /* taille de police plus compacte */
      line-height: 1.2;
      color-adjust: exact;
      -webkit-print-color-adjust: exact;
    }
    .section, .info-card, .flow-step {
      page-break-inside: avoid; /* évite les coupures gênantes */
    }
    /* Réduire marges internes des éléments */
    .container, .section {
      padding: 0.5rem;
    }
  `));
  document.head.appendChild(style);

  window.print(); // lance la boîte d'impression du navigateur
}

// Option: Bouton pour déclencher printCompact()
document.addEventListener('DOMContentLoaded', () => {
  const printBtn = document.createElement('button');
  printBtn.textContent = 'Imprimer PDF compact';
  printBtn.classList.add('print-button');
  printBtn.onclick = printCompact;
  document.body.appendChild(printBtn);
});
