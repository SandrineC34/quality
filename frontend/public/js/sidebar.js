// Load external sidebar markup
fetch('../../../partials/sidebar.html')
    .then(r => r.text())
    .then(html => {
        const aside = document.querySelector('aside.modern-sidebar');
        if (aside) aside.innerHTML = html;
    })
    .catch(err => console.error('Failed to load sidebar:', err));

const sbLinks = document.querySelectorAll('.sb-link');
const sections = document.querySelectorAll('.modern-content .section[id]');

function updateActiveLink() {
    let current = '';
    sections.forEach(s => {
        if (window.scrollY >= s.offsetTop - 90) current = s.id;
    });
    sbLinks.forEach(a => {
        const href = a.getAttribute('href');
        a.classList.toggle('active', href === '#' + current);
    });
}

window.addEventListener('scroll', updateActiveLink, { passive: true });
