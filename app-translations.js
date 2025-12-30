// Traduções para app.html (elementos críticos)
const appTranslations = {
    pt: {
        // Header
        title: 'Plataforma de Diligência Prévia Ambiental',
        subtitle: 'Plataforma de Diligência Prévia',
        status: 'Sistema Ativo',

        // Buttons
        drawBtn: 'Desenhar',
        clearBtn: 'Limpar',
        validateBtn: '🔍 Validar Área',
        exportBtn: '📥 Exportar GeoJSON',
        pdfBtn: '📄 Baixar Relatório PDF',
        confirmPdfBtn: '📄 Gerar Relatório PDF',
        sampleBtn: '🎯 Testar com Área de Exemplo',
        clearHistory: 'Limpar',

        // Search
        searchPlaceholder: 'Buscar cidade ou estado...',

        // Area info
        areaLabel: 'Área Selecionada',
        areaLimit: 'Limite: 10.000 ha',

        // Steps
        step1Title: 'Navegue e Defina a Área',
        step1Text: 'Use a busca, desenhe com o <strong>Lápis (✏️)</strong>, faça upload ou teste com área de exemplo. <span style="color:var(--accent-yellow); font-size:0.75rem;">Limite: 10.000 ha.</span>',
        step2Title: 'Validação Automática',
        step2Text: 'Clique em <strong>Validar Área</strong> para cruzamento instantâneo com 6 bases oficiais (PRODES, MapBiomas, TIs, Embargos, UCs, Quilombolas).',
        step3Title: 'Relatório PDF',
        step3Text: 'Baixe o relatório profissional com mapas, verificações detalhadas e QR Code de autenticidade. <strong>Requer API Key</strong>.',

        // Map legend
        legendTitle: 'Legenda',
        legendNeutral: 'Área Desenhada',
        legendApproved: 'Aprovado',
        legendRejected: 'Rejeitado',
        legendWarning: 'Atenção',

        // Data Freshness
        dataFreshness: 'Atualização dos Dados',

        // PDF Modal
        pdfModalTitle: 'Gerar Relatório PDF',
        pdfApiKeyLabel: 'API Key (obrigatória para PDF)',
        pdfApiKeyPlaceholder: 'Digite sua API key...',
        pdfPropertyLabel: 'Nome da Propriedade (opcional)',
        pdfPropertyPlaceholder: 'Ex: Fazenda Santa Rita',
        pdfPlotLabel: 'Nome do Talhão (opcional)',
        pdfPlotPlaceholder: 'Ex: Talhão 12',
        pdfLangLabel: 'Idioma do Relatório',
        pdfLangPt: 'Português',
        pdfLangEn: 'English',

        // Messages
        sampleLoaded: '✨ Área de exemplo carregada! Clique em "Validar Área" para testar sem API Key.',
        clearHistoryConfirm: 'Limpar histórico?',
        areaFileName: 'Área de Exemplo (Sinop, MT) - Validação livre',
        overlapLabel: '📍 Área Afetada:',

        // Validation results
        statusApproved: 'APROVADO',
        statusRejected: 'REJEITADO',
        statusWarning: 'ATENÇÃO',
        statusProcessing: 'Validando...',

        // Check items
        checkProdes: 'Desmatamento PRODES',
        checkMapbiomas: 'Alertas MapBiomas',
        checkIndigenous: 'Terras Indígenas',
        checkEmbargoes: 'Embargos IBAMA',
        checkQuilombola: 'Territórios Quilombolas',
        checkConservation: 'Unidades de Conservação',
        checkAmazon: 'Amazônia Legal',
        checkApp: 'Áreas de Preservação',

        // Sidebar cards
        authTitle: 'Autenticação',
        apiKeyPlaceholder: 'Cole sua API Key',
        apiKeyRequired: '✨ Explore o mapa gratuitamente! API Key necessária apenas para validar suas áreas.',
        getApiKey: 'Obtenha sua chave:',
        uploadTitle: 'Upload de Arquivo',
        uploadText: 'Toque para selecionar',
        uploadHint: 'GeoJSON ou JSON',
        historyTitle: 'Histórico',

        // Dynamic messages
        noPolygon: 'Nenhum polígono',
        polygonLoaded: 'Polígono carregado',
        geojsonExported: 'GeoJSON exportado!',
        validatingArea: 'Validando área...',
        connecting: 'Conectando',
        searching: 'Buscando...',
        noResults: 'Nenhum resultado',
        searchError: 'Erro na busca',
        historyEmpty: 'Nenhuma validação ainda',
        fillFarmPlot: 'Preencha Fazenda e Talhão',
        insertApiKey: 'Insira sua API Key para gerar o PDF',
        pdfGenerating: '⏳ Gerando...',
        pdfError: 'Erro ao gerar PDF',
        pdfSuccess: 'PDF gerado com sucesso!',
        errorUpload: 'Erro: ',
        compliance: 'Conformidade:',
    },
    en: {
        // Header
        title: 'Environmental Due Diligence Platform',
        subtitle: 'Due Diligence Platform',
        status: 'System Active',

        // Buttons
        drawBtn: 'Draw',
        clearBtn: 'Clear',
        validateBtn: '🔍 Validate Area',
        exportBtn: '📥 Export GeoJSON',
        pdfBtn: '📄 Download PDF Report',
        confirmPdfBtn: '📄 Generate PDF Report',
        sampleBtn: '🎯 Test with Sample Area',
        clearHistory: 'Clear',

        // Search
        searchPlaceholder: 'Search city or state...',

        // Area info
        areaLabel: 'Selected Area',
        areaLimit: 'Limit: 10,000 ha',

        // Steps
        step1Title: 'Navigate and Define Area',
        step1Text: 'Use search, draw with <strong>Pencil (✏️)</strong>, upload or test with sample area. <span style="color:var(--accent-yellow); font-size:0.75rem;">Limit: 10,000 ha.</span>',
        step2Title: 'Automatic Validation',
        step2Text: 'Click <strong>Validate Area</strong> for instant cross-check with 6 official databases (PRODES, MapBiomas, Indigenous Lands, Embargoes, Conservation Units, Quilombola).',
        step3Title: 'PDF Report',
        step3Text: 'Download professional report with maps, detailed checks and authenticity QR Code. <strong>Requires API Key</strong>.',

        // Map legend
        legendTitle: 'Legend',
        legendNeutral: 'Drawn Area',
        legendApproved: 'Approved',
        legendRejected: 'Rejected',
        legendWarning: 'Warning',

        // Data Freshness
        dataFreshness: 'Data Freshness',

        // PDF Modal
        pdfModalTitle: 'Generate PDF Report',
        pdfApiKeyLabel: 'API Key (required for PDF)',
        pdfApiKeyPlaceholder: 'Enter your API key...',
        pdfPropertyLabel: 'Property Name (optional)',
        pdfPropertyPlaceholder: 'Ex: Santa Rita Farm',
        pdfPlotLabel: 'Plot Name (optional)',
        pdfPlotPlaceholder: 'Ex: Plot 12',
        pdfLangLabel: 'Report Language',
        pdfLangPt: 'Português',
        pdfLangEn: 'English',

        // Messages
        sampleLoaded: '✨ Sample area loaded! Click "Validate Area" to test without API Key.',
        clearHistoryConfirm: 'Clear history?',
        areaFileName: 'Sample Area (Sinop, MT) - Free validation',
        overlapLabel: '📍 Affected Area:',

        // Validation results
        statusApproved: 'APPROVED',
        statusRejected: 'REJECTED',
        statusWarning: 'WARNING',
        statusProcessing: 'Validating...',

        // Check items
        checkProdes: 'PRODES Deforestation',
        checkMapbiomas: 'MapBiomas Alerts',
        checkIndigenous: 'Indigenous Lands',
        checkEmbargoes: 'IBAMA Embargoes',
        checkQuilombola: 'Quilombola Territories',
        checkConservation: 'Conservation Units',
        checkAmazon: 'Legal Amazon',
        checkApp: 'Preservation Areas',

        // Sidebar cards
        authTitle: 'Authentication',
        apiKeyPlaceholder: 'Paste your API Key',
        apiKeyRequired: '✨ Explore the map for free! API Key required only to validate your areas.',
        getApiKey: 'Get your key:',
        uploadTitle: 'File Upload',
        uploadText: 'Tap to select',
        uploadHint: 'GeoJSON or JSON',
        historyTitle: 'History',

        // Dynamic messages
        noPolygon: 'No polygon',
        polygonLoaded: 'Polygon loaded',
        geojsonExported: 'GeoJSON exported!',
        validatingArea: 'Validating area...',
        connecting: 'Connecting',
        searching: 'Searching...',
        noResults: 'No results',
        searchError: 'Search error',
        historyEmpty: 'No validations yet',
        fillFarmPlot: 'Fill in Farm and Plot',
        insertApiKey: 'Insert your API Key to generate PDF',
        pdfGenerating: '⏳ Generating...',
        pdfError: 'Error generating PDF',
        pdfSuccess: 'PDF generated successfully!',
        errorUpload: 'Error: ',
        compliance: 'Compliance:',
    }
};

// Sistema de tradução para app.html
(function() {
    let currentLang = localStorage.getItem('app_language') || 'pt';

    // Aplicar idioma inicial ao carregar a página
    document.addEventListener('DOMContentLoaded', () => {
        applyAppTranslations(currentLang);
        updateLangButton(currentLang);
    });

    // Função para aplicar traduções
    function applyAppTranslations(lang) {
        const t = appTranslations[lang];

        // Update document title
        document.title = t.title;

        // Update all elements with data-i18n-app attribute
        document.querySelectorAll('[data-i18n-app]').forEach(el => {
            const key = el.getAttribute('data-i18n-app');
            if (t[key]) {
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.placeholder = t[key];
                } else if (el.hasAttribute('title')) {
                    el.setAttribute('title', t[key]);
                } else {
                    el.innerHTML = t[key];
                }
            }
        });

        // Update HTML lang attribute
        document.documentElement.lang = lang === 'en' ? 'en' : 'pt-BR';

        // Store preference
        localStorage.setItem('app_language', lang);
        currentLang = lang;
    }

    // Função para atualizar o botão de idioma
    function updateLangButton(lang) {
        const langBtn = document.getElementById('langToggleApp');
        if (langBtn) {
            langBtn.textContent = lang.toUpperCase();
        }
    }

    // Expor funções globalmente para o botão poder chamar
    window.toggleAppLanguage = function() {
        const newLang = currentLang === 'pt' ? 'en' : 'pt';
        applyAppTranslations(newLang);
        updateLangButton(newLang);

        // Re-renderizar histórico com novo idioma
        if (typeof renderHistory === 'function') {
            renderHistory();
        }
    };

    window.getCurrentAppLang = function() {
        return currentLang;
    };

    // Função para obter tradução de uma chave específica
    window.getAppTranslation = function(key) {
        return appTranslations[currentLang]?.[key] || appTranslations['pt'][key] || key;
    };
})();
