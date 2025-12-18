# 🧪 Guia de Validação do GreenGate

**Antes de apresentar para QUALQUER cliente, você DEVE executar estes testes.**

Um falso positivo/negativo pode:
- ❌ Fazer cliente perder negócio de R$ 5 milhões
- ❌ Gerar responsabilidade legal
- ❌ Destruir sua reputação antes de começar

---

## 📋 CHECKLIST DE VALIDAÇÃO

### ✅ Etapa 1: Verificar Dados (5 minutos)

```bash
cd backend
python validate_against_official_sources.py
```

**O que este script faz:**
- ✅ Verifica se existem dados no Supabase
- ✅ Mostra quantidade de registros por camada
- ✅ Verifica data de atualização
- ✅ Compara com fontes oficiais conhecidas

**Resultado esperado:**
```
✅ TODOS OS CHECKS PASSARAM!
   Sistema está pronto para testes com clientes.
```

**Se falhar:**
- ❌ Você NÃO tem dados suficientes
- ❌ Precisa popular o banco primeiro
- ❌ Veja `scripts/import_reference_data.py`

---

### ✅ Etapa 2: Testar Casos Conhecidos (10 minutos)

```bash
cd backend
python test_validation_accuracy.py
```

**O que este script faz:**
- 🧪 Testa 3 áreas conhecidas:
  1. Área limpa (deve aprovar)
  2. Terra Indígena (deve reprovar)
  3. Unidade de Conservação (deve reprovar)
- 📊 Calcula taxa de acerto
- 🎯 Mostra onde errou (se errou)

**Resultado esperado:**
```
📊 RELATÓRIO DE PRECISÃO
Acertos:   3/3
Precisão:  100.0%

🎉 EXCELENTE! Sistema 100% preciso nos testes.
   Você pode apresentar para clientes com confiança.
```

**Critérios de aprovação:**
- ✅ **100%** → Excelente, pode lançar
- ⚠️  **80-99%** → Bom, mas revise os erros
- ❌ **< 80%** → NÃO lance, tem problemas críticos

---

### ✅ Etapa 3: Testar com Áreas Reais (1-2 horas)

**MUITO IMPORTANTE:** Teste com áreas que **você conhece o resultado**.

#### 3.1. Peça para Amigos/Conhecidos

Pegue 5-10 fazendas reais de amigos/família/conhecidos:
- ✅ De preferência com CAR
- ✅ Que já fizeram análise ambiental
- ✅ Que você sabe se tem problema ou não

#### 3.2. Execute Validação

1. Desenhe a área no mapa (www.greengate.com.br)
2. Baixe o relatório PDF
3. Compare com a realidade:
   - Se tem embargo, o GreenGate detectou?
   - Se está em TI, o GreenGate detectou?
   - Se é área limpa, o GreenGate aprovou?

#### 3.3. Calcule Precisão Real

```
Precisão = Acertos / Total de Testes

Exemplo:
- 8 acertos de 10 testes = 80% de precisão
- 9 acertos de 10 testes = 90% de precisão
- 10 acertos de 10 testes = 100% de precisão
```

**Meta mínima:** 95% de precisão

---

### ✅ Etapa 4: Casos Limite (30 min - 1 hora)

Teste **casos difíceis** que podem gerar falso positivo/negativo:

#### 4.1. Áreas Muito Pequenas (< 1 ha)
- Precisão GPS pode gerar falso positivo
- APP de rio pode pegar área por imprecisão

**Como testar:**
```python
# Adicione em test_validation_accuracy.py:
{
    "name": "Área Muito Pequena (0.5 ha)",
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-55.500, -11.860],
            [-55.499, -11.860],
            [-55.499, -11.861],
            [-55.500, -11.861],
            [-55.500, -11.860]
        ]]
    },
    "expected": {"status": "approved", "should_have_issues": False}
}
```

#### 4.2. Áreas na Borda de TI/UC
- Testar se detecta sobreposição mínima
- Ou se ignora (depende do threshold)

#### 4.3. Áreas com Desmatamento Antigo (antes de 2008)
- PRODES só tem dados de 2008+
- Se desmatou em 2005, não deve reprovar

---

## 📊 COMO INTERPRETAR RESULTADOS

### ✅ Cenário Ideal (PODE LANÇAR)

```
✅ Dados: 10.000+ registros em 5+ camadas
✅ Precisão: 100% (3/3 casos de teste)
✅ Áreas reais: 9/10 acertos (90%)
✅ Casos limite: Funciona conforme esperado
```

**Ação:** Pode apresentar para primeiros clientes Beta com confiança.

---

### ⚠️  Cenário Bom (PODE LANÇAR COM RESSALVAS)

```
✅ Dados: 5.000+ registros em 4+ camadas
⚠️  Precisão: 66% (2/3 casos de teste) - 1 erro
✅ Áreas reais: 8/10 acertos (80%)
⚠️  Casos limite: Alguns falsos positivos em áreas pequenas
```

**Ação:**
1. Documente as limitações no relatório
2. Adicione disclaimer sobre áreas < 1 ha
3. Lance com clientes Beta conscientes das limitações
4. Itere com feedback

---

### ❌ Cenário Crítico (NÃO LANCE)

```
❌ Dados: < 1.000 registros
❌ Precisão: 33% (1/3 casos de teste) - 2 erros
❌ Áreas reais: 5/10 acertos (50%)
❌ Casos limite: Muitos falsos positivos/negativos
```

**Ação:**
1. ❌ NÃO apresente para clientes
2. 🔍 Investigue os erros:
   - Dados estão corretos?
   - Lógica de threshold está certa?
   - PostGIS está calculando área corretamente?
3. 🔧 Corrija os problemas
4. 🔄 Execute validação novamente

---

## 🐛 DEBUG: Quando Algo Está Errado

### Problema: "Nenhum dado encontrado"

```bash
# Verificar se Supabase está conectado
cd backend/backend
python -c "from app.core.config import settings; print(settings.DATABASE_URL)"

# Verificar se tabelas existem
psql $DATABASE_URL -c "SELECT COUNT(*) FROM reference_layers;"
```

### Problema: "Sempre retorna 'aprovado'"

**Causa provável:** Banco vazio (falso negativo)

**Solução:**
1. Verificar se `reference_layers` tem dados
2. Verificar se `is_active = true`
3. Popular banco com scripts de importação

### Problema: "Sempre retorna 'reprovado'"

**Causa provável:** Threshold muito baixo (falso positivo)

**Solução:**
1. Verificar `OVERLAP_THRESHOLDS` em `validation_engine.py`
2. Ajustar para ignorar sobreposições < 0.01 ha (imprecisão GPS)
3. Testar novamente

### Problema: "Precisão baixa (< 80%)"

**Investigar:**
1. Quais checks estão errando?
2. É sempre o mesmo check?
3. Dados desatualizados?
4. Geometrias inválidas?

**Exemplo de debug:**
```python
# Adicione logs em validation_engine.py
log.info(f"Overlap: {overlap['total_area_ha']} ha - {overlap['percentage']:.2f}%")
```

---

## 📝 DOCUMENTAÇÃO PARA CLIENTE

**Após validação bem-sucedida**, documente:

### 1. Taxa de Precisão

```
Taxa de Acerto: 95%
Testado com: 20 áreas reais
Período: Janeiro 2025
```

### 2. Limitações Conhecidas

```
- Áreas < 0.5 ha: Precisão GPS pode gerar alertas
- Dados PRODES: Disponíveis desde 2008
- Atualização: Dados de dezembro/2024
```

### 3. Disclaimer no Relatório

```
Este relatório é baseado em bases oficiais públicas
com data de atualização especificada.

Precisão testada: 95%
Última validação: 15/01/2025

Para decisões críticas, recomenda-se validação
complementar com visita in loco.
```

---

## 🎯 CRITÉRIOS DE APROVAÇÃO FINAL

Antes de apresentar para clientes, **TODOS** devem estar ✅:

- [ ] ✅ Dados populados (> 5.000 registros)
- [ ] ✅ Precisão em casos teste: 100%
- [ ] ✅ Precisão em áreas reais: >= 90%
- [ ] ✅ Casos limite documentados
- [ ] ✅ Disclaimer no relatório
- [ ] ✅ Comparado com fontes oficiais
- [ ] ✅ Testado por pelo menos 2 pessoas diferentes

**Se TODOS estiverem ✅:**
🎉 **PODE LANÇAR!**

**Se ALGUM estiver ❌:**
🚨 **NÃO LANCE AINDA**

---

## 📞 Quando Pedir Ajuda

Se após executar os testes você encontrar:
- ❌ Precisão < 80%
- ❌ Falsos negativos em áreas com embargo/TI conhecidos
- ❌ Sistema sempre retorna "aprovado"

**Entre em contato com:**
- GitHub Issues: https://github.com/Josue2747/GreenGate/issues
- Email: [seu email de suporte]

**Inclua:**
- Output dos scripts de validação
- Coordenadas da área que deu erro
- Resultado esperado vs. obtido
