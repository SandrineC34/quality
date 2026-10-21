// Load external navigation markup
fetch('../../../partials/header.html')
    .then(r => r.text())
    .then(html => {
        const nav = document.getElementById('navMenuWrap');
        if (nav) nav.innerHTML = html;
    })
    .catch(err => console.error('Failed to load navigation:', err));

function toggleMenu() {
    const wrap = document.getElementById('navMenuWrap');
    const btn  = document.querySelector('.menu-toggle');
    wrap.classList.toggle('open');
    btn.setAttribute('aria-expanded', wrap.classList.contains('open'));
}

function toggleSubmenu(e) {
    e.stopPropagation();
    e.currentTarget.classList.toggle('submenu-open');
}
