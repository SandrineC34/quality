/**
 * headerfooter.js - 
 */

// --- PARTIE 1 : CHARGEMENT DYNAMIQUE DU HEADER ET FOOTER ---
function fixRelativePaths(html) {
    const path = window.location.pathname;
    const htmlIdx = path.indexOf('/html/');
    if (htmlIdx === -1) return html;
    const afterHtml = path.substring(htmlIdx + 6);
    const segments = afterHtml.split('/').filter(s => s.length > 0);
    const dirDepth = segments.length - 1;
    const neededLevels = dirDepth + 1;
    const currentLevels = 2;
    const extraLevels = neededLevels - currentLevels;
    if (extraLevels <= 0) return html;
    const replacement = '../'.repeat(neededLevels);
    return html.replace(/(href|src)="\.\.\/\.\.\//g, '$1="' + replacement);
}

function loadHTML(containerId, url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors du chargement de ' + url);
            }
            return response.text();
        })
        .then(html => {
            const container = document.getElementById(containerId);
            if (container) {
                container.innerHTML = fixRelativePaths(html);
            }
        })
        .catch(error => {
            console.error('Erreur de chargement:', error);
        });
}

function getRelativePath() {
    const currentPath = window.location.pathname;
    if (currentPath.includes('/Infrastructure/Cloud_INRAE_Toulouse/')) {
        return { header: '../../../footer-header/header.html', footer: '../../../footer-header/footer.html' };
    }
    else if (currentPath.includes('/Infrastructure/')) {
        return { header: '../../footer-header/header.html', footer: '../../footer-header/footer.html' };
    }
    else if (currentPath.includes('/Processus/')) {
        return { header: '../../footer-header/header.html', footer: '../../footer-header/footer.html' };
    }
    else if (currentPath.includes('/Parties_interresees/')) {
        return { header: '../footer-header/header.html', footer: '../footer-header/footer.html' };
    }
    else if (
        currentPath.includes('/Cartographie/') || currentPath.includes('/Organigramme/') ||
        currentPath.includes('/Enjeux/') || currentPath.includes('/Politique/')
    ) {
        return { header: '../footer-header/header.html', footer: '../footer-header/footer.html' };
    }
    else if (currentPath.includes('/Logigrammes/')) {
        return { header: '../footer-header/header.html', footer: '../footer-header/footer.html' };
    }
    else {
        return { header: 'footer-header/header.html', footer: 'footer-header/footer.html' };
    }
}

// --- PARTIE 2 : ÉDITION ET FILTRAGE CLAVIER ULTRA-STRICT ---
document.addEventListener('DOMContentLoaded', function() {
    const paths = getRelativePath();
    loadHTML('header', paths.header);
    loadHTML('footer', paths.footer);

    // Ajout du bouton de sauvegarde
    // const btn = document.createElement('button');
    // btn.id = 'smq-save-btn';
    // btn.innerText = '💾 Enregistrer sur GitLab';
    // btn.style = "position: fixed; top: 20px; right: 20px; background-color: #27ae60; color: white; border: none; padding: 10px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; z-index: 10000; box-shadow: 0 2px 5px rgba(0,0,0,0.2);";
    // document.body.appendChild(btn);

    // BLOCAGE EN AMONT : On neutralise le comportement de la touche Entrée globalement sur les zones éditables
    document.addEventListener('keypress', (e) => {
        const activeEl = document.activeElement;
        if (activeEl && activeEl.hasAttribute('contenteditable') && activeEl.tagName === 'DIV') {
            if (e.key === 'Enter' || e.keyCode === 13) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        }
    }, true);

    // INTERCEPTION PHRASE DE CAPTURE (PRINCIPALE)
    document.addEventListener('keydown', (e) => {
        const activeEl = document.activeElement;
        
        if (activeEl && activeEl.hasAttribute('contenteditable') && activeEl.tagName === 'DIV') {
            
            // --- TOUCHE ENTRÉE (Génère une seule ligne et y téléporte le curseur) ---
            if (e.key === 'Enter' || e.keyCode === 13) {
                e.preventDefault();
                e.stopImmediatePropagation();
                
                const newRow = document.createElement('div');
                newRow.className = activeEl.className; // Conserve la classe de couleur
                newRow.setAttribute('contenteditable', 'true');
                newRow.innerHTML = '&#8203;'; // Caractère invisible (ZWNBSP) pour forcer l'existence de la ligne
                
                // Insertion immédiate
                activeEl.parentNode.insertBefore(newRow, activeEl.nextSibling);
                
                // Téléportation manuelle et immédiate du curseur dans la nouvelle ligne unique
                const range = document.createRange();
                const sel = window.getSelection();
                range.setStart(newRow, 0);
                range.collapse(true);
                sel.removeAllRanges();
                sel.addRange(range);
                
                newRow.focus();
                return false;
            }
            
            // --- TOUCHE RETOUR ARRIÈRE ---
            if (e.key === 'Backspace' || e.keyCode === 8) {
                // On considère la case vide si elle ne contient rien ou seulement notre caractère invisible
                const text = activeEl.innerText.replace(/\u200B/g, '').trim();
                if (text === '') {
                    e.preventDefault();
                    e.stopImmediatePropagation();
                    
                    const previousRow = activeEl.previousElementSibling;
                    const parent = activeEl.parentNode;
                    const premierMotClasse = activeEl.className.split(' ')[0];
                    
                    if (parent.querySelectorAll(`.${premierMotClasse}`).length > 1) {
                        activeEl.remove();
                        
                        if (previousRow && previousRow.hasAttribute('contenteditable')) {
                            previousRow.focus();
                            const range = document.createRange();
                            const sel = window.getSelection();
                            range.selectNodeContents(previousRow);
                            range.collapse(false);
                            sel.removeAllRanges();
                            sel.addRange(range);
                        }
                    }
                    return false;
                }
            }
        }
    }, true);

    // --- PARTIE 3 : SAUVEGARDE API GITLAB ---
    btn.addEventListener('click', async () => {
        const token = prompt("Veuillez saisir votre Token d'accès GitLab :");
        if (!token) return alert("Enregistrement annulé.");

        const commitMessage = prompt("Motif du changement (Exigence ISO 9001) :");
        if (!commitMessage) return alert("Enregistrement annulé.");

        const projectId = "VOTRE_ID_NUMERIQUE_PROJET_GITLAB"; // À remplacer par votre ID projet fixe
        const filePath = window.location.pathname.split('/').pop(); 
        const branch = "main"; 

        const cloneDoc = document.documentElement.cloneNode(true);
        
        // Nettoyage complet des caractères invisibles injectés avant sauvegarde
        cloneDoc.querySelectorAll('[contenteditable="true"]').forEach(el => {
            el.innerHTML = el.innerHTML.replace(/\u200B/g, '');
        });

        const saveBtn = cloneDoc.querySelector('#smq-save-btn');
        if (saveBtn) saveBtn.remove();

        const htmlContent = "<!DOCTYPE html>\n" + cloneDoc.outerHTML;
        const url = `https://gitlab.com/api/v4/projects/${projectId}/repository/files/${encodeURIComponent(filePath)}`;
        
        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: { 'PRIVATE-TOKEN': token, 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    branch: branch,
                    commit_message: commitMessage,
                    content: btoa(unescape(encodeURIComponent(htmlContent))),
                    encoding: "base64"
                })
            });

            if (response.ok) {
                alert("✅ Modification enregistrée avec succès !");
                window.location.reload();
            } else {
                const errorData = await response.json();
                alert(`❌ Erreur GitLab : ${errorData.message}`);
            }
        } catch (error) {
            alert(`❌ Erreur réseau : ${error.message}`);
        }
    });
});