// Sistema de tradução completo PT/EN
(function() {
    const langToggle = document.getElementById('langToggle');
    const langText = document.getElementById('langText');

    // Detectar idioma inicial
    let currentLang = localStorage.getItem('language') || 'pt';

    // Aplicar idioma inicial
    applyTranslations(currentLang);
    langText.textContent = currentLang.toUpperCase();

    // Toggle de idioma
    langToggle.addEventListener('click', () => {
        currentLang = currentLang === 'pt' ? 'en' : 'pt';
        applyTranslations(currentLang);
        langText.textContent = currentLang.toUpperCase();
        localStorage.setItem('language', currentLang);
    });

    function applyTranslations(lang) {
        const t = translations[lang];

        // Navigation
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (t[key]) {
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.placeholder = t[key];
                } else {
                    el.textContent = t[key];
                }
            }
        });

        // Hero title (pode ter HTML)
        const heroTitle = document.querySelector('[data-i18n-html="hero_title"]');
        if (heroTitle && t.hero_title) {
            heroTitle.innerHTML = t.hero_title;
        }

        // Pricing price (formato especial)
        const priceEl = document.querySelector('[data-i18n="pricing_api_price"]');
        if (priceEl && t.pricing_api_price) {
            priceEl.innerHTML = t.pricing_api_price + ' <small>' + t.pricing_api_per + '</small>';
        }

        // ROI savings
        const roiSaved = document.querySelector('[data-i18n="pricing_roi_saved"]');
        if (roiSaved && t.pricing_roi_saved) {
            roiSaved.innerHTML = 'R$ 24.910 <small>' + t.pricing_roi_saved + '</small>';
        }
    }
})();
