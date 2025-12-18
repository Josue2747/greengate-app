"""
Testa se a API key funciona (valida o hash)
"""
import asyncio
import sys
import hashlib
from pathlib import Path

# Adicionar backend ao path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

print("=" * 80)
print("🔍 TESTAR VALIDAÇÃO DE API KEY")
print("=" * 80)
print()

api_key_input = input("Cole a API key completa aqui: ").strip()

if not api_key_input:
    print("❌ Você precisa colar a API key!")
    exit()

print()
print(f"API Key fornecida: {api_key_input[:12]}...")
print()

async def testar():
    try:
        from app.core.database import async_session_maker
        from app.services.api_key_service import APIKeyService

        async with async_session_maker() as db:
            service = APIKeyService(db)

            # Hash da key fornecida
            key_hash = hashlib.sha256(api_key_input.encode()).hexdigest()
            print(f"Hash calculado: {key_hash[:16]}...")
            print()

            # Tentar verificar
            print("Verificando no banco...")
            api_key_record = await service.verify_api_key(api_key_input)

            if api_key_record:
                print()
                print("=" * 80)
                print("✅ API KEY VÁLIDA!")
                print("=" * 80)
                print()
                print(f"  Cliente: {api_key_record.client_name}")
                print(f"  Plano: {api_key_record.plan}")
                print(f"  Quota mensal: {api_key_record.monthly_quota or 'ILIMITADO'}")
                print(f"  Ativa: {api_key_record.is_active}")
                print(f"  Revogada: {api_key_record.is_revoked}")
                print(f"  Requests este mês: {api_key_record.requests_this_month}")
                print()

                # Verificar quota
                quota_info = await service.check_quota(api_key_record)
                print("Quota:")
                print(f"  Tem quota disponível: {quota_info['has_quota']}")
                print(f"  Quota restante: {quota_info.get('quota_remaining', 'ILIMITADO')}")
                print()

                if quota_info['has_quota']:
                    print("✅ API key funcionaria normalmente!")
                else:
                    print("❌ QUOTA EXCEDIDA!")

            else:
                print()
                print("=" * 80)
                print("❌ API KEY INVÁLIDA!")
                print("=" * 80)
                print()
                print("Possíveis causas:")
                print("  1. API key não existe no banco")
                print("  2. API key foi revogada")
                print("  3. Hash não confere")
                print()

                # Buscar por prefixo para debug
                from sqlalchemy import select
                from app.models.api_key import APIKey

                prefix = api_key_input[:12] + "..."
                result = await db.execute(
                    select(APIKey).where(APIKey.key_prefix == prefix)
                )
                key_by_prefix = result.scalar_one_or_none()

                if key_by_prefix:
                    print("🔍 DEBUG: Encontrei uma key com esse prefixo no banco:")
                    print(f"  Hash no banco: {key_by_prefix.key_hash[:16]}...")
                    print(f"  Hash calculado: {key_hash[:16]}...")
                    print(f"  Hashes conferem: {key_by_prefix.key_hash == key_hash}")
                else:
                    print("🔍 DEBUG: Não encontrei nenhuma key com esse prefixo")

    except Exception as e:
        print()
        print("=" * 80)
        print("❌ ERRO AO TESTAR")
        print("=" * 80)
        print()
        print(f"Erro: {e}")
        print()
        import traceback
        traceback.print_exc()

asyncio.run(testar())

print()
print("=" * 80)
input("Pressione Enter para sair...")
