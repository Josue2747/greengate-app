"""
Gera SQL para inserir API key diretamente no banco (produção)
"""
import secrets
import hashlib
from datetime import datetime

print("=" * 80)
print("🔑 GERAR SQL PARA INSERIR API KEY NO BANCO DE PRODUCAO")
print("=" * 80)
print()

# Gerar API key
api_key = f"gg_live_{secrets.token_hex(16)}"
key_hash = hashlib.sha256(api_key.encode()).hexdigest()
key_prefix = api_key[:12] + "..."

# Dados
client_name = input("Nome do cliente: ").strip() or "Cliente Producao"
plan_num = input("Plano (1=FREE, 2=PRO, 3=ENTERPRISE) [1]: ").strip() or "1"

if plan_num == "1":
    plan = "free"
    quota = 1
elif plan_num == "2":
    plan = "professional"
    quota = 50
else:
    plan = "enterprise"
    quota = "NULL"  # ilimitado

print()
print("=" * 80)
print("SQL GERADO - COPIE E COLE NO BANCO DE PRODUCAO:")
print("=" * 80)
print()
print(f"""
-- ============================================================================
-- INSERIR API KEY: {key_prefix}
-- ============================================================================

INSERT INTO api_keys (
    key_hash,
    key_prefix,
    client_name,
    plan,
    monthly_quota,
    is_active,
    is_revoked,
    total_requests,
    requests_this_month
) VALUES (
    '{key_hash}',
    '{key_prefix}',
    '{client_name}',
    '{plan}',
    {quota},
    true,
    false,
    0,
    0
);

-- Verificar se foi inserido
SELECT key_prefix, client_name, plan, monthly_quota, is_active
FROM api_keys
WHERE key_prefix = '{key_prefix}';
""")

print()
print("=" * 80)
print("⚠️  IMPORTANTE - COPIE ESTA API KEY AGORA!")
print("=" * 80)
print()
print(f"🔑 API KEY: {api_key}")
print()
print("Esta é a ÚNICA vez que você vai ver essa key!")
print()
print("=" * 80)
print()
print("📍 ONDE RODAR ESSE SQL:")
print()
print("1. Entre no Railway (dashboard.railway.app)")
print("2. Abra seu projeto GreenGate")
print("3. Clique no banco de dados")
print("4. Clique em 'Query' ou 'Data'")
print("5. Cole o SQL acima")
print("6. Execute")
print()
print("OU se o Railway usa Supabase:")
print("1. Entre no Supabase")
print("2. Abra SQL Editor")
print("3. Cole o SQL")
print("4. Execute")
print()
print("=" * 80)
print()
input("Pressione Enter para sair...")
