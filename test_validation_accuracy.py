"""
GreenGate - Script de Validação de Precisão

Este script testa se o sistema está gerando falsos positivos/negativos.

COMO USAR:
1. cd backend
2. python test_validation_accuracy.py

O que ele faz:
- Verifica se existem dados nas tabelas de referência
- Testa com áreas conhecidas (Terra Indígena, Embargo, etc.)
- Compara resultado com expectativa
- Gera relatório de precisão
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório backend ao path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings
from app.models.schemas import GeoJSONPolygon
from app.services.validation_engine import GeoValidationEngine


# ============================================================
# ÁREAS DE TESTE (Coordenadas Conhecidas)
# ============================================================

TEST_CASES = [
    {
        "name": "Área Limpa (Exemplo Genérico)",
        "description": "Área sem restrições conhecidas (centro do MT, área agrícola)",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-55.52, -11.86],
                [-55.48, -11.86],
                [-55.48, -11.88],
                [-55.52, -11.88],
                [-55.52, -11.86]
            ]]
        },
        "expected": {
            "status": "approved",  # Esperamos que passe
            "should_have_issues": False,
        }
    },
    {
        "name": "Terra Indígena Xingu (MT)",
        "description": "Dentro do Parque Indígena do Xingu - DEVE REPROVAR",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-53.5, -12.0],
                [-53.4, -12.0],
                [-53.4, -12.1],
                [-53.5, -12.1],
                [-53.5, -12.0]
            ]]
        },
        "expected": {
            "status": "rejected",
            "should_have_issues": True,
            "expected_check": "terra_indigena",
        }
    },
    {
        "name": "Unidade de Conservação - PARNA Chapada dos Veadeiros (GO)",
        "description": "Dentro de UC de Proteção Integral - DEVE REPROVAR",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-47.6, -14.1],
                [-47.5, -14.1],
                [-47.5, -14.2],
                [-47.6, -14.2],
                [-47.6, -14.1]
            ]]
        },
        "expected": {
            "status": "rejected",
            "should_have_issues": True,
            "expected_check": "uc",
        }
    },
]


# ============================================================
# VERIFICAÇÃO DE DADOS
# ============================================================

async def check_database_health(session: AsyncSession) -> dict:
    """
    Verifica se existem dados nas tabelas de referência.
    """
    print("\n" + "="*60)
    print("📊 VERIFICANDO DADOS NO BANCO")
    print("="*60 + "\n")

    results = {}

    layers = [
        ("prodes", "Desmatamento PRODES"),
        ("mapbiomas", "MapBiomas Alertas"),
        ("terra_indigena", "Terras Indígenas"),
        ("embargo_ibama", "Embargos IBAMA"),
        ("quilombola", "Territórios Quilombolas"),
        ("uc", "Unidades de Conservação"),
        ("hidrografia", "Hidrografia/APP"),
    ]

    for layer_type, name in layers:
        query = text("""
            SELECT COUNT(*) as count
            FROM reference_layers
            WHERE layer_type = :layer_type AND is_active = true
        """)
        result = await session.execute(query, {"layer_type": layer_type})
        count = result.scalar()

        status = "✅" if count > 0 else "❌"
        results[layer_type] = count

        print(f"{status} {name:30} → {count:>6} registros")

    print()
    total_records = sum(results.values())

    if total_records == 0:
        print("🚨 CRÍTICO: NENHUM DADO ENCONTRADO!")
        print("   O sistema vai SEMPRE retornar 'aprovado' (falso negativo).")
        print()
        print("   Você precisa popular o banco com dados reais.")
        print("   Veja: backend/scripts/import_reference_data.py")
    elif total_records < 100:
        print("⚠️  ATENÇÃO: Poucos dados encontrados.")
        print("   Resultados podem não ser representativos.")
    else:
        print(f"✅ Total: {total_records} registros em {len([v for v in results.values() if v > 0])} camadas")

    return results


# ============================================================
# TESTE DE CASOS
# ============================================================

async def test_validation_accuracy(session: AsyncSession):
    """
    Testa áreas conhecidas e verifica se o sistema acerta.
    """
    print("\n" + "="*60)
    print("🧪 TESTANDO CASOS DE VALIDAÇÃO")
    print("="*60 + "\n")

    engine = GeoValidationEngine(session)
    results = []

    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n📍 TESTE {i}/{len(TEST_CASES)}: {test_case['name']}")
        print(f"   {test_case['description']}")
        print()

        try:
            # Executar validação
            geom = GeoJSONPolygon(**test_case['geometry'])
            result = await engine.validate_polygon(geom)

            # Comparar com expectativa
            expected_status = test_case['expected']['status']
            actual_status = result.status.value

            is_correct = actual_status == expected_status

            # Exibir resultado
            status_icon = "✅" if is_correct else "❌"
            print(f"   Status Esperado: {expected_status}")
            print(f"   Status Obtido:   {actual_status}")
            print(f"   Score:           {result.risk_score}/100")
            print(f"   Resultado:       {status_icon} {'CORRETO' if is_correct else 'INCORRETO'}")

            # Detalhes dos checks
            print(f"\n   Verificações:")
            for check in result.checks:
                check_icon = "✓" if check.status.value == "pass" else "✗" if check.status.value == "fail" else "⊘"
                overlap_text = f" ({check.overlap_area_ha:.2f} ha)" if check.overlap_area_ha else ""
                print(f"      {check_icon} {check.check_type.value:25} → {check.status.value}{overlap_text}")

            results.append({
                "name": test_case['name'],
                "expected": expected_status,
                "actual": actual_status,
                "correct": is_correct,
                "score": result.risk_score,
            })

        except Exception as e:
            print(f"   ❌ ERRO: {e}")
            results.append({
                "name": test_case['name'],
                "expected": expected_status,
                "actual": "error",
                "correct": False,
                "error": str(e),
            })

    # Relatório Final
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE PRECISÃO")
    print("="*60 + "\n")

    correct = sum(1 for r in results if r['correct'])
    total = len(results)
    accuracy = (correct / total * 100) if total > 0 else 0

    print(f"Acertos:   {correct}/{total}")
    print(f"Precisão:  {accuracy:.1f}%")
    print()

    if accuracy == 100:
        print("🎉 EXCELENTE! Sistema 100% preciso nos testes.")
        print("   Você pode apresentar para clientes com confiança.")
    elif accuracy >= 80:
        print("✅ BOM! Sistema está funcionando bem.")
        print("   Mas revise os casos que erraram antes de lançar.")
    elif accuracy >= 50:
        print("⚠️  MÉDIO. Sistema tem problemas.")
        print("   NÃO apresente para clientes ainda.")
    else:
        print("🚨 CRÍTICO! Sistema não está funcionando.")
        print("   Verifique dados e lógica de validação.")

    return results


# ============================================================
# MAIN
# ============================================================

async def main():
    print("\n" + "="*60)
    print("🌿 GREENGATE - VALIDAÇÃO DE PRECISÃO")
    print("="*60)

    # Conectar ao banco
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # 1. Verificar se existem dados
        data_health = await check_database_health(session)

        total_records = sum(data_health.values())

        if total_records == 0:
            print("\n⚠️  IMPOSSÍVEL TESTAR SEM DADOS.")
            print("   Popule o banco primeiro e execute novamente.")
            return

        # 2. Testar casos conhecidos
        results = await test_validation_accuracy(session)

    await engine.dispose()

    print("\n" + "="*60)
    print("✅ VALIDAÇÃO CONCLUÍDA")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
