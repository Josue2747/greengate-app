// Sistema de tradução PT/EN completo
const translations = {
    pt: {
        // Navigation
        nav_features: 'Funcionalidades',
        nav_pricing: 'Preços',
        nav_contact: 'Contato',
        nav_docs: 'Documentação API',
        nav_cta: 'Começar Agora',

        // Hero
        hero_title: 'Validação Geoespacial para Conformidade Ambiental',
        hero_subtitle: 'Desenhe ou envie sua área e cruze com 7 camadas oficiais de dados ambientais brasileiros. Gere relatório PDF auditável em até 2 minutos.',
        hero_cta: 'Testar Gratuitamente',
        hero_docs: 'Ver Documentação',
        hero_check1: 'Desmatamento (PRODES)',
        hero_check2: 'Terras Indígenas (FUNAI)',
        hero_check3: 'Unidades de Conservação',
        hero_check4: 'Embargos Ambientais (IBAMA)',
        hero_check5: 'Territórios Quilombolas (INCRA)',
        hero_check6: 'Amazônia Legal',
        hero_check7: 'Recursos Hídricos (ANA)',

        // Features
        features_title: 'Por Que GreenGate?',
        features_subtitle: 'Transparência e auditabilidade em conformidade ambiental',

        feature1_title: 'Resultado Reproduzível',
        feature1_desc: 'Mesma área + mesma data = mesmo resultado. Validações determinísticas sem margem para interpretação.',

        feature2_title: 'Sem Falhas por Arquivos Corrompidos',
        feature2_desc: 'Validação geométrica automática via PostGIS. Polígonos inválidos são detectados e corrigidos antes do processamento.',

        feature3_title: 'Fontes Oficiais Rastreáveis',
        feature3_desc: 'Todas as camadas provêm de órgãos oficiais (INPE, FUNAI, IBAMA, ICMBio, INCRA, ANA, MapBiomas). Auditável e defensável.',

        // How We Validate
        validate_title: 'Como Validamos',
        validate_subtitle: 'Metodologia transparente e auditável',

        validate1_title: 'Método Reproduzível',
        validate1_desc: 'Mesma área + mesma data = mesmo resultado sempre',

        validate2_title: 'Fontes Oficiais',
        validate2_desc: 'INPE, FUNAI, IBAMA, ICMBio, INCRA, ANA, MapBiomas',

        validate3_title: 'Data de Atualização',
        validate3_desc: 'Cada camada exibe quando foi atualizada pela última vez',

        validate4_title: 'Validação Automática',
        validate4_desc: 'Geometrias validadas via PostGIS antes do cruzamento',

        // Data Sources
        data_title: 'Camadas de Dados Oficiais',
        data_subtitle: 'Integração com as principais fontes governamentais',

        data1_title: 'PRODES (INPE)',
        data1_year: 'Versão 2023',
        data1_desc: 'Desmatamento na Amazônia Legal',

        data2_title: 'Terras Indígenas (FUNAI)',
        data2_year: 'Versão 2024',
        data2_desc: 'Demarcações homologadas e em processo',

        data3_title: 'Unidades de Conservação (ICMBio)',
        data3_year: 'Versão 2024',
        data3_desc: 'Proteção integral e uso sustentável',

        data4_title: 'Embargos IBAMA',
        data4_year: 'Versão 2024',
        data4_desc: 'Áreas com restrição ambiental',

        data5_title: 'Territórios Quilombolas (INCRA)',
        data5_year: 'Versão 2023',
        data5_desc: 'Comunidades tradicionais tituladas',

        data6_title: 'Amazônia Legal',
        data6_year: 'Versão Oficial',
        data6_desc: 'Área sujeita a legislação especial',

        // Pricing
        pricing_title: 'Preços',
        pricing_subtitle: 'Transparente e previsível',

        pricing_manual_title: 'Análise Técnica Manual',
        pricing_manual_desc: 'Processo tradicional',
        pricing_manual_price: 'R$ 265',
        pricing_manual_per: '/validação',
        pricing_manual_time: '2-5 dias por validação',
        pricing_manual_feat1: 'Análise técnica especializada',
        pricing_manual_feat2: 'Verificação manual de cada camada',
        pricing_manual_feat3: 'Relatório técnico descritivo',
        pricing_manual_feat4: 'Custo de equipe especializada',
        pricing_manual_feat5: 'Escalabilidade limitada',

        pricing_api_title: 'GreenGate API',
        pricing_api_desc: 'Validação automatizada',
        pricing_api_price: 'R$ 15,90',
        pricing_api_per: '/validação',
        pricing_api_saving: 'Preço fixo por validação',
        pricing_api_feat1: '< 2 minutos por validação',
        pricing_api_feat2: '6 camadas oficiais integradas',
        pricing_api_feat3: 'API REST pronta para uso',
        pricing_api_feat4: 'Processamento otimizado PostGIS',
        pricing_api_feat5: 'Geometrias sempre validadas',
        pricing_api_feat6: 'Relatório PDF auditável',
        pricing_api_feat7: 'QR Code para verificação pública',
        pricing_api_feat8: 'Rastreabilidade completa',
        pricing_api_fixed: 'Preço Fixo:',
        pricing_api_fixed_desc: 'R$ 15,90 por validação, sem variação por volume.',
        pricing_api_fixed_simple: 'Simples, transparente e previsível.',

        pricing_roi_title: 'Seu ROI',
        pricing_roi_desc: 'Exemplo: 100 validações/mês',
        pricing_roi_saved: '/mês economizados',
        pricing_roi_feat1: 'Custo análise técnica: R$ 26.500/mês',
        pricing_roi_feat2: 'Custo GreenGate: R$ 1.590/mês',
        pricing_roi_feat3: 'Economia: R$ 24.910/mês',
        pricing_roi_feat4: 'Redução de custos: 94%',
        pricing_roi_feat5: 'Payback: Imediato (1ª validação)',
        pricing_roi_feat6: 'Tempo economizado: 200-400h/mês',
        pricing_roi_feat7: 'Equipe livre para análises estratégicas',
        pricing_roi_note: '* Cálculo baseado em R$ 265 médio por validação manual e preço fixo de R$ 15,90/validação',

        pricing_example_title: 'Ver Exemplo de Relatório',
        pricing_example_desc: 'PDF de demonstração com validação real',
        pricing_example_link: 'Baixar PDF de Exemplo',
        pricing_example_info: 'Relatório real de fazenda exemplo com QR Code funcional para verificação pública.',

        // Contact
        contact_title: 'Fale Conosco',
        contact_subtitle: 'Tire suas dúvidas ou solicite acesso à API',

        contact_label_name: 'Nome',
        contact_placeholder_name: 'João Silva',
        contact_label_email: 'E-mail',
        contact_placeholder_email: 'joao@empresa.com.br',
        contact_label_company: 'Empresa',
        contact_placeholder_company: 'Sua Empresa Ltda',
        contact_label_message: 'Mensagem',
        contact_placeholder_message: 'Como podemos ajudar?',
        contact_submit: 'Enviar Mensagem',

        contact_info_title: 'Informações de Contato',
        contact_email: 'E-mail',
        contact_phone: 'Telefone',
        contact_hours: 'Horário',
        contact_hours_value: 'Seg-Sex: 9h-18h (horário de Brasília)',

        // Footer
        footer_desc: 'Plataforma de validação geoespacial para conformidade ambiental e anti-desmatamento.',
        footer_product: 'Produto',
        footer_features: 'Funcionalidades',
        footer_pricing: 'Preços',
        footer_docs: 'Documentação',
        footer_support: 'Suporte',
        footer_contact: 'Contato',
        footer_faq: 'FAQ',
        footer_legal: 'Legal',
        footer_privacy: 'Política de Privacidade',
        footer_terms: 'Termos de Uso',
        footer_rights: '© 2025 GreenGate. Todos os direitos reservados.',

        // Messages
        form_sending: 'Enviando...',
        form_success: '✓ Mensagem enviada com sucesso! Entraremos em contato em breve.',
        form_error: '✗ Erro ao enviar mensagem. Tente novamente.'
    },
    en: {
        // Navigation
        nav_features: 'Features',
        nav_pricing: 'Pricing',
        nav_contact: 'Contact',
        nav_docs: 'API Documentation',
        nav_cta: 'Get Started',

        // Hero
        hero_title: 'Geospatial Validation for Environmental Compliance',
        hero_subtitle: 'Draw or upload your area and cross-check with 7 official Brazilian environmental data layers. Generate auditable PDF report in under 2 minutes.',
        hero_cta: 'Try Free',
        hero_docs: 'View Documentation',
        hero_check1: 'Deforestation (PRODES)',
        hero_check2: 'Indigenous Lands (FUNAI)',
        hero_check3: 'Conservation Units',
        hero_check4: 'Environmental Embargoes (IBAMA)',
        hero_check5: 'Quilombola Territories (INCRA)',
        hero_check6: 'Legal Amazon',
        hero_check7: 'Water Resources (ANA)',

        // Features
        features_title: 'Why GreenGate?',
        features_subtitle: 'Transparency and auditability in environmental compliance',

        feature1_title: 'Reproducible Results',
        feature1_desc: 'Same area + same date = same result. Deterministic validations with no room for interpretation.',

        feature2_title: 'No Failures from Corrupted Files',
        feature2_desc: 'Automatic geometric validation via PostGIS. Invalid polygons are detected and corrected before processing.',

        feature3_title: 'Traceable Official Sources',
        feature3_desc: 'All layers come from official agencies (INPE, FUNAI, IBAMA, ICMBio, INCRA, ANA, MapBiomas). Auditable and defensible.',

        // How We Validate
        validate_title: 'How We Validate',
        validate_subtitle: 'Transparent and auditable methodology',

        validate1_title: 'Reproducible Method',
        validate1_desc: 'Same area + same date = same result always',

        validate2_title: 'Official Sources',
        validate2_desc: 'INPE, FUNAI, IBAMA, ICMBio, INCRA, ANA, MapBiomas',

        validate3_title: 'Update Date',
        validate3_desc: 'Each layer displays when it was last updated',

        validate4_title: 'Automatic Validation',
        validate4_desc: 'Geometries validated via PostGIS before cross-checking',

        // Data Sources
        data_title: 'Official Data Layers',
        data_subtitle: 'Integration with key government sources',

        data1_title: 'PRODES (INPE)',
        data1_year: 'Version 2023',
        data1_desc: 'Deforestation in the Legal Amazon',

        data2_title: 'Indigenous Lands (FUNAI)',
        data2_year: 'Version 2024',
        data2_desc: 'Homologated and in-process demarcations',

        data3_title: 'Conservation Units (ICMBio)',
        data3_year: 'Version 2024',
        data3_desc: 'Full protection and sustainable use',

        data4_title: 'IBAMA Embargoes',
        data4_year: 'Version 2024',
        data4_desc: 'Areas with environmental restrictions',

        data5_title: 'Quilombola Territories (INCRA)',
        data5_year: 'Version 2023',
        data5_desc: 'Titled traditional communities',

        data6_title: 'Legal Amazon',
        data6_year: 'Official Version',
        data6_desc: 'Area subject to special legislation',

        // Pricing
        pricing_title: 'Pricing',
        pricing_subtitle: 'Transparent and predictable',

        pricing_manual_title: 'Manual Technical Analysis',
        pricing_manual_desc: 'Traditional process',
        pricing_manual_price: 'R$ 265',
        pricing_manual_per: '/validation',
        pricing_manual_time: '2-5 days per validation',
        pricing_manual_feat1: 'Specialized technical analysis',
        pricing_manual_feat2: 'Manual verification of each layer',
        pricing_manual_feat3: 'Descriptive technical report',
        pricing_manual_feat4: 'Specialized team cost',
        pricing_manual_feat5: 'Limited scalability',

        pricing_api_title: 'GreenGate API',
        pricing_api_desc: 'Automated validation',
        pricing_api_price: 'R$ 15.90',
        pricing_api_per: '/validation',
        pricing_api_saving: 'Fixed price per validation',
        pricing_api_feat1: '< 2 minutes per validation',
        pricing_api_feat2: '6 integrated official layers',
        pricing_api_feat3: 'Ready-to-use REST API',
        pricing_api_feat4: 'Optimized PostGIS processing',
        pricing_api_feat5: 'Always validated geometries',
        pricing_api_feat6: 'Auditable PDF report',
        pricing_api_feat7: 'QR Code for public verification',
        pricing_api_feat8: 'Complete traceability',
        pricing_api_fixed: 'Fixed Price:',
        pricing_api_fixed_desc: 'R$ 15.90 per validation, no volume variation.',
        pricing_api_fixed_simple: 'Simple, transparent, and predictable.',

        pricing_roi_title: 'Your ROI',
        pricing_roi_desc: 'Example: 100 validations/month',
        pricing_roi_saved: '/month saved',
        pricing_roi_feat1: 'Technical analysis cost: R$ 26,500/month',
        pricing_roi_feat2: 'GreenGate cost: R$ 1,590/month',
        pricing_roi_feat3: 'Savings: R$ 24,910/month',
        pricing_roi_feat4: 'Cost reduction: 94%',
        pricing_roi_feat5: 'Payback: Immediate (1st validation)',
        pricing_roi_feat6: 'Time saved: 200-400h/month',
        pricing_roi_feat7: 'Team free for strategic analysis',
        pricing_roi_note: '* Calculation based on R$ 265 average per manual validation and fixed price of R$ 15.90/validation',

        pricing_example_title: 'View Example Report',
        pricing_example_desc: 'Demonstration PDF with real validation',
        pricing_example_link: 'Download Example PDF',
        pricing_example_info: 'Real report from example farm with functional QR Code for public verification.',

        // Contact
        contact_title: 'Contact Us',
        contact_subtitle: 'Ask questions or request API access',

        contact_label_name: 'Name',
        contact_placeholder_name: 'John Smith',
        contact_label_email: 'Email',
        contact_placeholder_email: 'john@company.com',
        contact_label_company: 'Company',
        contact_placeholder_company: 'Your Company Ltd',
        contact_label_message: 'Message',
        contact_placeholder_message: 'How can we help?',
        contact_submit: 'Send Message',

        contact_info_title: 'Contact Information',
        contact_email: 'Email',
        contact_phone: 'Phone',
        contact_hours: 'Hours',
        contact_hours_value: 'Mon-Fri: 9am-6pm (Brasília time)',

        // Footer
        footer_desc: 'Geospatial validation platform for environmental compliance and anti-deforestation.',
        footer_product: 'Product',
        footer_features: 'Features',
        footer_pricing: 'Pricing',
        footer_docs: 'Documentation',
        footer_support: 'Support',
        footer_contact: 'Contact',
        footer_faq: 'FAQ',
        footer_legal: 'Legal',
        footer_privacy: 'Privacy Policy',
        footer_terms: 'Terms of Use',
        footer_rights: '© 2025 GreenGate. All rights reserved.',

        // Messages
        form_sending: 'Sending...',
        form_success: '✓ Message sent successfully! We will contact you soon.',
        form_error: '✗ Error sending message. Please try again.'
    }
};
