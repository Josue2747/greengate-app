"""
Script SUPER SIMPLES para configurar conexão com Supabase
Só executar: python configurar_supabase.py
"""
from pathlib import Path

print("=" * 80)
print("🔧 CONFIGURAR CONEXÃO COM SUPABASE")
print("=" * 80)
print()
print("📍 Onde encontrar a URL do Supabase:")
print("   1. Acesse https://supabase.com e entre no seu projeto")
print("   2. Clique em 'Project Settings' (ícone de engrenagem)")
print("   3. Clique em 'Database'")
print("   4. Procure 'Connection string' → escolha 'URI'")
print("   5. Copie a URL (vai ser algo como: postgresql://postgres.xxxx:senha@...)")
print()
print("-" * 80)
print()

# Pedir URL
url = input("📝 Cole aqui a URL do Supabase: ").strip()

if not url:
    print("❌ Você precisa colar a URL!")
    exit()

# Validar
if not ("postgres" in url and "@" in url):
    print("❌ Essa não parece ser uma URL válida!")
    print("   Deve ser algo como: postgresql://postgres.xxxxx:senha@aws-0-us-east-1.pooler.supabase.com:5432/postgres")
    exit()

# Converter para formato asyncpg
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql+asyncpg://", 1)
elif url.startswith("postgresql://") and "+asyncpg" not in url:
    url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

print()
print("✅ URL configurada:")
print(f"   {url[:50]}...")
print()

# Ler .env.example
env_example = Path(__file__).parent / ".env.example"
env_file = Path(__file__).parent / ".env"

if not env_example.exists():
    print("❌ Arquivo .env.example não encontrado!")
    exit()

# Ler conteúdo do .env.example
content = env_example.read_text(encoding="utf-8")

# Substituir DATABASE_URL
lines = []
for line in content.split("\n"):
    if line.startswith("DATABASE_URL="):
        lines.append(f"DATABASE_URL={url}")
    else:
        lines.append(line)

# Escrever .env
env_file.write_text("\n".join(lines), encoding="utf-8")

print("=" * 80)
print("✅ ✅ ✅ ARQUIVO .env CRIADO COM SUCESSO! ✅ ✅ ✅")
print("=" * 80)
print()
print(f"📄 Arquivo salvo em: {env_file}")
print()
print("🚀 PRÓXIMOS PASSOS:")
print()
print("   1. Criar a tabela no banco:")
print("      cd backend")
print("      alembic upgrade head")
print()
print("   2. Testar se a API sobe:")
print("      python backend/app/main.py")
print()
print("   3. Criar primeira API key:")
print("      cd ..")
print("      python criar_minha_primeira_key.py")
print()
print("=" * 80)
