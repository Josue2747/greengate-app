"""
Script SUPER SIMPLES para criar sua primeira API key
Só executar: python criar_minha_primeira_key.py
"""
import asyncio
import sys
from pathlib import Path

# Adicionar backend ao path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

print("=" * 80)
print("🔑 CRIAR API KEY DO GREENGATE")
print("=" * 80)
print()

# Perguntar dados básicos
nome = input("📝 Nome do cliente (ex: Fazenda Santa Maria): ").strip()
if not nome:
    print("❌ Você precisa digitar um nome!")
    exit()

print()
print("💰 Escolha o plano:")
print("   1 = FREE (1 validação para teste)")
print("   2 = PROFISSIONAL (50 validações por mês)")
print("   3 = EMPRESARIAL (ILIMITADO)")
print()

plano_num = input("Digite 1, 2 ou 3: ").strip()

if plano_num == "1":
    plano = "free"
    quota = 1
elif plano_num == "2":
    plano = "professional"
    quota = 50
elif plano_num == "3":
    plano = "enterprise"
    quota = "ILIMITADO"
else:
    print("❌ Opção inválida! Digite 1, 2 ou 3")
    exit()

print()
print("✅ Confirmação:")
print(f"   Cliente: {nome}")
print(f"   Plano: {plano.upper()}")
print(f"   Validações/mês: {quota}")
print()

confirma = input("Confirma? (s/n): ").strip().lower()
if confirma != 's':
    print("❌ Cancelado.")
    exit()

print()
print("⏳ Criando API key no banco de dados...")
print()


async def criar():
    """Cria a API key."""
    try:
        from app.core.database import async_session_maker
        from app.services.api_key_service import APIKeyService

        async with async_session_maker() as db:
            service = APIKeyService(db)

            result = await service.create_api_key(
                client_name=nome,
                plan=plano,
            )

            print("=" * 80)
            print("✅ ✅ ✅ API KEY CRIADA COM SUCESSO! ✅ ✅ ✅")
            print("=" * 80)
            print()
            print("⚠️  ATENÇÃO: COPIE E GUARDE ESTA API KEY AGORA!")
            print("⚠️  ELA NÃO SERÁ MOSTRADA NOVAMENTE!")
            print()
            print("-" * 80)
            print(f"🔑 API KEY: {result['api_key']}")
            print("-" * 80)
            print()
            print("📋 Informações:")
            print(f"   Cliente: {result['client_name']}")
            print(f"   Plano: {result['plan'].upper()}")
            print(f"   Validações/mês: {result['monthly_quota'] or 'ILIMITADO'}")
            print(f"   Criado em: {result['created_at']}")
            print()
            print("=" * 80)
            print()
            print("💡 Como usar esta API key:")
            print()
            print("   No seu código ou POSTMAN, adicione o header:")
            print(f'   x-api-key: {result["api_key"]}')
            print()
            print("   Exemplo com curl:")
            print('   curl -X POST https://api.greengate.com.br/api/v1/validations/quick \\')
            print('     -H "Content-Type: application/json" \\')
            print(f'     -H "x-api-key: {result["api_key"]}" \\')
            print("     -d '{\"type\": \"Polygon\", \"coordinates\": [...]}'")
            print()
            print("=" * 80)

    except Exception as e:
        print()
        print("=" * 80)
        print("❌ ERRO AO CRIAR API KEY")
        print("=" * 80)
        print()
        print(f"Erro: {e}")
        print()
        print("🔍 Possíveis causas:")
        print("   1. Migration não foi rodada (precisa criar tabela api_keys)")
        print("      Solução: rode 'alembic upgrade head'")
        print()
        print("   2. Banco de dados não está acessível")
        print("      Solução: verifique .env com DATABASE_URL")
        print()
        print("   3. Pacotes não instalados")
        print("      Solução: rode 'pip install -r requirements.txt'")
        print()
        import traceback
        traceback.print_exc()


# Executar
asyncio.run(criar())
