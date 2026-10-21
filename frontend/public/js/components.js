const LEGENDES_PROCESSUS = {
    // Manangement
    "P1-O1": [
        { code: "sp1", text: "SP1 – Pilotage stratégique" },
        { code: "sp2", text: "SP2 – SMQ" },
        { code: "sp3", text: "SP3 – Communication" }
    ],
    //Accompagnement 
    "P2-O1": [
        { code: "sp1", text: "SP1 – Traitement des demandes" },
        { code: "sp2", text: "SP2 – Formation &amp; dissémination" },
        { code: "sp3", text: "SP3 – Accompagnement à l'utilisation" }
    ],
    //Developpement
    "P2-O2": [
        { code: "sp1", text: "SP1 – Développement" },
        { code: "sp3", text: "SP2 – Conception" }
    ],
    //Infrastructure
    "P2-O3": [
        { code: "sp1", text: "SP1 – Création d'Infrastructure" },
        { code: "sp2", text: "SP2 – MCO & Supervision" },
        { code: "sp3", text: "SP3 – Déploiement instances" }
    ],

    //Ressources
    "P3-O1": [
        { code: "sp1", text: "SP1 – Ressources Humaines" },
        { code: "sp2", text: "SP2 – Logistique" },
        { code: "sp3", text: "SP3 – Formation" },
        { code: "sp4", text: "SP4 – Évaluation des fournisseurs" }
    ]

};

// Normalise l'ID (majuscules, "0" -> "O" dans le suffixe) pour tolérer P2-03 / P2-O3
const normaliserId = id => (id || "").trim().toUpperCase().replace(/-0/g, "-O");

document.addEventListener("DOMContentLoaded", () => {
    const processId = normaliserId(document.body.dataset.processId);
    const cle = Object.keys(LEGENDES_PROCESSUS).find(k => normaliserId(k) === processId);
    const items = cle && LEGENDES_PROCESSUS[cle];

    if (!items) return;

    const htmlContent = `
        <div class="io-legend" style="margin-bottom:0.9rem;">
            <span style="font-weight:600; color:#64748b;">Périmètre :</span>
            ${items.map(item => `<span class="io-legend-item"><span class="io-legend-dot ${item.code}"></span> ${item.text}</span>`).join('')}
        </div>
    `;

    document.querySelectorAll('.io-legend-target').forEach(el => {
        el.innerHTML = htmlContent;
    });
});