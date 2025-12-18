#!/bin/bash
# ========================================
# Script de Setup para Railway
# ========================================
# Execute no Railway Shell:
# bash setup-railway.sh

set -e  # Para na primeira falha

echo "🚀 Iniciando setup do GreenGate no Railway..."

# 1. Instalar dependências do admin
echo ""
echo "📦 Instalando dependências do painel admin..."
pip install -r requirements-admin.txt

# 2. Rodar migrations (criar índices de performance)
echo ""
echo "🗄️  Rodando migrations (criando índices de performance)..."
alembic upgrade head

echo ""
echo "✅ Setup concluído com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configurar variáveis de ambiente (ver RAILWAY-ENV-VARS.txt)"
echo "2. Baixar admin-panel.html e configurar API_URL"
echo "3. Acessar painel admin e criar suas API keys"
echo ""
echo "🎉 Sistema pronto para uso!"
