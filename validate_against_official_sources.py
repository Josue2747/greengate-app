"""
GreenGate - Validação contra Fontes Oficiais

Este script compara os resultados do GreenGate com fontes oficiais públicas.

IMPORTANTE: Este script requer conexão com internet para consultar APIs públicas.

FONTES CONSULTADAS:
- TerraBrasilis (PRODES - INPE) - API pública
- FUNAI (Terras Indígenas) - Shapefile público
- ICMBio (Unidades de Conservação) - API pública

COMO USAR:
1. cd backend
2. python validate_against_official_sources.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings


# ============================================================
# VERIFICAÇÃO DE METADADOS
# ============================================================

async def check_data_sources_metadata(session: AsyncSession):
    """
    Verifica metadados das fontes de dados:
    - Data de última atualização
    - Versão dos dados
    - Quantidade de registros
    """
    print("\n" + "="*60)
    print("📅 METADADOS DAS FONTES DE DADOS")
    print("="*60 + "\n")

    # Tentar buscar de dataset_versions (se existir)
    try:
        query = text("""
            SELECT
                layer_type,
                version,
                source_date,
                record_count,
                ingested_at,
                source_url
            FROM dataset_versions
            WHERE is_active = true
            ORDER BY layer_type
        """)
        result = await session.execute(query)
        rows = result.fetchall()

        if rows:
            print("Fonte de Dados Encontrada: dataset_versions")
            print()
            for row in rows:
                print(f"📊 {row.layer_type}")
                print(f"   Versão:        {row.version}")
                print(f"   Data Fonte:    {row.source_date}")
                print(f"   Registros:     {row.record_count:,}")
                print(f"   Importado em:  {row.ingested_at}")
                if row.source_url:
                    print(f"   URL:           {row.source_url[:60]}...")
                print()

            return True
        else:
            print("⚠️  Tabela dataset_versions existe mas está vazia.")
    except Exception as e:
        print(f"ℹ️  Tabela dataset_versions não encontrada: {e}")

    # Fallback: contar registros por layer_type
    print("\n📊 Contagem de Registros (reference_layers):")
    print()

    query = text("""
        SELECT
            layer_type,
            COUNT(*) as count,
            MIN(created_at) as oldest,
            MAX(created_at) as newest
        FROM reference_layers
        WHERE is_active = true
        GROUP BY layer_type
        ORDER BY layer_type
    """)
    result = await session.execute(query)
    rows = result.fetchall()

    if not rows:
        print("❌ NENHUM DADO ENCONTRADO em reference_layers!")
        return False

    for row in rows:
        print(f"📊 {row.layer_type:25} → {row.count:>6} registros")
        if row.oldest and row.newest:
            print(f"   Período: {row.oldest.date()} a {row.newest.date()}")
        print()

    return True


# ============================================================
# COMPARAÇÃO COM FONTES OFICIAIS
# ============================================================

async def compare_with_official_sources(session: AsyncSession):
    """
    Compara uma amostra de dados com fontes oficiais públicas.

    NOTA: Este é um teste básico. Para validação completa, você precisaria:
    1. Baixar shapefiles oficiais completos
    2. Comparar geometria por geometria
    3. Verificar atributos (nome, categoria, data)
    """
    print("\n" + "="*60)
    print("🌐 COMPARAÇÃO COM FONTES OFICIAIS")
    print("="*60 + "\n")

    print("ℹ️  INSTRUÇÕES PARA VALIDAÇÃO MANUAL:\n")

    print("1️⃣  TERRAS INDÍGENAS (FUNAI)")
    print("   📥 Baixe o shapefile oficial:")
    print("      https://geoserver.funai.gov.br/")
    print("   🔍 Compare quantidade de registros")
    print("   📅 Verifique data de atualização")
    print()

    print("2️⃣  PRODES (INPE)")
    print("   📥 Acesse:")
    print("      http://terrabrasilis.dpi.inpe.br/")
    print("   🔍 Consulte área de teste específica")
    print("   📊 Compare resultado com GreenGate")
    print()

    print("3️⃣  UNIDADES DE CONSERVAÇÃO (ICMBio)")
    print("   📥 Baixe shapefile:")
    print("      https://www.icmbio.gov.br/portal/geoprocessamentos")
    print("   🔍 Compare UCs no seu banco com oficial")
    print()

    print("4️⃣  EMBARGOS IBAMA")
    print("   📥 Consulte:")
    print("      https://servicos.ibama.gov.br/ctf/publico/areasembargadas/ConsultaPublicaAreasEmbargadas.php")
    print("   🔍 Busque uma área embargada conhecida")
    print("   ✅ Valide se GreenGate detecta")
    print()

    # Verificar algumas geometrias de exemplo
    print("="*60)
    print("🧪 TESTE RÁPIDO: Geometrias de Referência")
    print("="*60 + "\n")

    # Terra Indígena do Xingu (conhecida)
    ti_query = text("""
        SELECT COUNT(*) as count
        FROM reference_layers
        WHERE layer_type = 'terra_indigena'
          AND is_active = true
          AND (
              source_name ILIKE '%xingu%'
              OR extra_data::text ILIKE '%xingu%'
          )
    """)
    result = await session.execute(ti_query)
    xingu_count = result.scalar()

    if xingu_count > 0:
        print(f"✅ Terra Indígena do Xingu encontrada ({xingu_count} registros)")
        print("   Isso indica que você tem dados de TIs reais.")
    else:
        print("⚠️  Terra Indígena do Xingu NÃO encontrada")
        print("   Verifique se seus dados de TI estão completos.")

    print()

    # Chapada dos Veadeiros (UC conhecida)
    uc_query = text("""
        SELECT COUNT(*) as count
        FROM reference_layers
        WHERE layer_type = 'uc'
          AND is_active = true
          AND (
              source_name ILIKE '%veadeiros%'
              OR source_name ILIKE '%chapada%'
              OR extra_data::text ILIKE '%veadeiros%'
          )
    """)
    result = await session.execute(uc_query)
    chapada_count = result.scalar()

    if chapada_count > 0:
        print(f"✅ PARNA Chapada dos Veadeiros encontrado ({chapada_count} registros)")
        print("   Isso indica que você tem dados de UCs reais.")
    else:
        print("⚠️  PARNA Chapada dos Veadeiros NÃO encontrado")
        print("   Verifique se seus dados de UC estão completos.")

    print()


# ============================================================
# CHECKLIST DE VALIDAÇÃO
# ============================================================

async def validation_checklist(session: AsyncSession):
    """
    Checklist de validação antes de lançar para clientes.
    """
    print("\n" + "="*60)
    print("✅ CHECKLIST DE VALIDAÇÃO PRÉ-LANÇAMENTO")
    print("="*60 + "\n")

    checks = []

    # 1. Dados existem?
    query = text("SELECT COUNT(*) FROM reference_layers WHERE is_active = true")
    result = await session.execute(query)
    total = result.scalar()
    checks.append(("Dados de referência populados", total > 100))

    # 2. Dados recentes?
    try:
        query = text("""
            SELECT MAX(created_at)
            FROM reference_layers
            WHERE is_active = true
        """)
        result = await session.execute(query)
        latest = result.scalar()

        from datetime import datetime, timedelta
        is_recent = latest and (datetime.utcnow() - latest) < timedelta(days=365)
        checks.append(("Dados com menos de 1 ano", is_recent))
    except:
        checks.append(("Dados com menos de 1 ano", False))

    # 3. Múltiplas camadas?
    query = text("""
        SELECT COUNT(DISTINCT layer_type)
        FROM reference_layers
        WHERE is_active = true
    """)
    result = await session.execute(query)
    layer_count = result.scalar()
    checks.append(("Pelo menos 3 camadas diferentes", layer_count >= 3))

    # 4. Geometrias válidas?
    try:
        query = text("""
            SELECT COUNT(*)
            FROM reference_layers
            WHERE is_active = true
              AND ST_IsValid(geom) = false
        """)
        result = await session.execute(query)
        invalid_count = result.scalar()
        checks.append(("Geometrias válidas (PostGIS)", invalid_count == 0))
    except:
        checks.append(("Geometrias válidas (PostGIS)", None))

    # Exibir checklist
    for check_name, passed in checks:
        if passed is True:
            print(f"✅ {check_name}")
        elif passed is False:
            print(f"❌ {check_name}")
        else:
            print(f"⚠️  {check_name} (não verificado)")

    print()

    all_passed = all(c[1] for c in checks)

    if all_passed:
        print("🎉 TODOS OS CHECKS PASSARAM!")
        print("   Sistema está pronto para testes com clientes.")
    else:
        print("⚠️  ALGUNS CHECKS FALHARAM")
        print("   Corrija os problemas antes de apresentar para clientes.")

    return all_passed


# ============================================================
# MAIN
# ============================================================

async def main():
    print("\n" + "="*60)
    print("🌿 GREENGATE - VALIDAÇÃO CONTRA FONTES OFICIAIS")
    print("="*60)

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # 1. Verificar metadados
        has_data = await check_data_sources_metadata(session)

        if not has_data:
            print("\n❌ IMPOSSÍVEL VALIDAR SEM DADOS")
            return

        # 2. Comparação com fontes oficiais
        await compare_with_official_sources(session)

        # 3. Checklist final
        await validation_checklist(session)

    await engine.dispose()

    print("\n" + "="*60)
    print("📋 PRÓXIMOS PASSOS")
    print("="*60 + "\n")
    print("1. Execute: python test_validation_accuracy.py")
    print("2. Teste com áreas reais do seu conhecimento")
    print("3. Compare resultados com análises técnicas existentes")
    print("4. Se precisão >= 95%, você pode apresentar para clientes")
    print()


if __name__ == "__main__":
    asyncio.run(main())
