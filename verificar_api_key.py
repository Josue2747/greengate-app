"""
Script para verificar se a API key foi criada corretamente no banco
"""
import asyncio
import sys
from pathlib import Path

# Adicionar backend ao path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

print("=" * 80)
print("🔍 VERIFICANDO API KEYS NO BANCO")
print("=" * 80)
print()

async def verificar():
    try:
        from app.core.database import async_session_maker
        from sqlalchemy import select, text
        from app.models.api_key import APIKey

        async with async_session_maker() as db:
            # Contar total de API keys
            result = await db.execute(select(APIKey))
            keys = result.scalars().all()

            print(f"✅ Total de API keys no banco: {len(keys)}")
            print()

            if len(keys) == 0:
                print("❌ NENHUMA API KEY ENCONTRADA!")
                print()
                print("Possível causa:")
                print("  - O script criar_minha_primeira_key.py não salvou no banco")
                print("  - Conectou em banco diferente")
                print()
                return

            # Mostrar detalhes de cada key
            for i, key in enumerate(keys, 1):
                print(f"API Key #{i}:")
                print(f"  Prefixo: {key.key_prefix}")
                print(f"  Cliente: {key.client_name}")
                print(f"  Plano: {key.plan}")
                print(f"  Quota mensal: {key.monthly_quota or 'ILIMITADO'}")
                print(f"  Requests este mês: {key.requests_this_month}")
                print(f"  Total requests: {key.total_requests}")
                print(f"  Ativa: {key.is_active}")
                print(f"  Revogada: {key.is_revoked}")
                print(f"  Criada em: {key.created_at}")
                print(f"  Expira em: {key.expires_at or 'NUNCA'}")
                print(f"  Último uso: {key.last_used_at or 'NUNCA USADA'}")
                print()

            # Verificar conexão com DATABASE_URL
            print("-" * 80)
            print("📊 Informações do banco:")
            print("-" * 80)
            result = await db.execute(text("SELECT current_database(), current_user"))
            db_name, db_user = result.fetchone()
            print(f"  Banco: {db_name}")
            print(f"  Usuário: {db_user}")
            print()

    except Exception as e:
        print("=" * 80)
        print("❌ ERRO AO VERIFICAR API KEYS")
        print("=" * 80)
        print()
        print(f"Erro: {e}")
        print()
        import traceback
        traceback.print_exc()

asyncio.run(verificar())

print("=" * 80)
print()
input("Pressione Enter para sair...")
