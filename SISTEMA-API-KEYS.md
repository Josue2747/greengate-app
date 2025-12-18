# Sistema de API Keys - GreenGate

## Visão Geral

Sistema completo de autenticação e controle de quotas via API Keys para a API GreenGate de validação geoespacial.

## Arquitetura

### Componentes

1. **Modelo de Dados** (`app/models/api_key.py`)
   - Tabela `api_keys` no PostgreSQL
   - Armazena hash SHA256 da API key (não plaintext)
   - Campos de controle: quota, contadores, timestamps

2. **Service Layer** (`app/services/api_key_service.py`)
   - Lógica de negócio: criar, validar, revogar keys
   - Incremento atômico de contadores (evita race conditions)
   - Suporte a 3 planos: Free, Professional, Enterprise

3. **Middleware** (`app/middleware/api_key_tracker.py`)
   - Intercepta todas as requisições
   - Valida API key e verifica quota
   - Usa SELECT FOR UPDATE (lock pessimista)
   - Adiciona headers de quota nas respostas

4. **Admin API** (`app/api/admin_api_keys.py`)
   - Endpoints para gerenciar API keys
   - Criar, listar, revogar keys
   - Estatísticas de uso

## Planos Disponíveis

| Plano         | Quota Mensal | Preço   | Descrição                    |
|---------------|--------------|---------|------------------------------|
| Free          | 1            | R$ 0    | 1 validação única para teste |
| Professional  | 50           | R$ 197  | 50 validações por mês        |
| Enterprise    | Ilimitado    | R$ 497  | Validações ilimitadas        |

## Formato da API Key

```
gg_live_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

- Prefixo: `gg_live_`
- 32 caracteres hexadecimais aleatórios
- Exemplo: `gg_live_3f7a9b2c5e8d1f4a6b9c2e5f8a1d4b7c`

## Como Criar uma API Key

### Opção 1: Script Python (Recomendado)

```bash
cd backend
python criar_minha_primeira_key.py
```

Interface interativa em português que guia pela criação.

### Opção 2: Script Admin

```bash
cd backend
python -m app.scripts.create_api_key \
  --client-name "Nome do Cliente" \
  --plan professional \
  --email cliente@email.com
```

### Opção 3: Diretamente no Banco (Produção)

Para criar keys em produção sem acesso local:

```sql
-- Gerar hash da API key (fazer localmente)
-- Exemplo: echo -n "gg_live_SUACHAVEAQUI" | sha256sum

INSERT INTO api_keys (
    id,
    key_hash,
    key_prefix,
    client_name,
    client_email,
    plan,
    monthly_quota,
    is_active,
    created_at
) VALUES (
    gen_random_uuid(),
    'HASH_SHA256_DA_KEY',
    'gg_live_XXX...',
    'Nome do Cliente',
    'email@cliente.com',
    'professional',
    50,
    true,
    NOW()
);
```

⚠️ **IMPORTANTE**: A API key em plaintext só é mostrada UMA VEZ na criação. Não é possível recuperá-la depois!

## Como Usar a API Key

### No Frontend (JavaScript)

```javascript
const API_KEY = 'gg_live_sua_chave_aqui';

const response = await fetch('https://api.greengate.com.br/api/v1/validations/quick', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY  // ← Header obrigatório
    },
    body: JSON.stringify({
        type: 'Polygon',
        coordinates: [...]
    })
});
```

### Via cURL

```bash
curl -X POST https://api.greengate.com.br/api/v1/validations/quick \
  -H "Content-Type: application/json" \
  -H "x-api-key: gg_live_sua_chave_aqui" \
  -d '{"type":"Polygon","coordinates":[...]}'
```

### Via Python

```python
import requests

headers = {
    'Content-Type': 'application/json',
    'x-api-key': 'gg_live_sua_chave_aqui'
}

response = requests.post(
    'https://api.greengate.com.br/api/v1/validations/quick',
    headers=headers,
    json={'type': 'Polygon', 'coordinates': [...]}
)
```

## Headers de Quota na Resposta

Todas as respostas incluem headers informativos:

```
X-RateLimit-Limit: 50              # Quota mensal total
X-RateLimit-Remaining: 37          # Quota restante
X-RateLimit-Reset: 1735689600      # Timestamp do próximo reset
```

## Códigos de Status HTTP

| Status | Descrição                                    |
|--------|----------------------------------------------|
| 200    | Validação realizada com sucesso              |
| 401    | API Key inválida ou expirada                 |
| 403    | API Key não fornecida                        |
| 429    | Quota mensal excedida                        |
| 500    | Erro interno do servidor                     |

## Mensagens de Erro

### 403 - Sem API Key
```json
{
  "detail": "API Key não fornecida. Use o header x-api-key."
}
```

### 401 - API Key Inválida
```json
{
  "detail": "API Key inválida ou expirada."
}
```

### 429 - Quota Excedida
```json
{
  "detail": "Quota mensal excedida. Limite: 50, Usado: 50. Faça upgrade do plano ou aguarde o reset mensal."
}
```

## Gerenciamento via SQL

### Verificar Status de uma Key

```sql
SELECT
    key_prefix,
    client_name,
    plan,
    monthly_quota,
    requests_this_month,
    total_requests,
    last_used_at,
    is_active,
    is_revoked
FROM api_keys
WHERE key_prefix = 'gg_live_XXX...';
```

### Resetar Contador de Quota

```sql
UPDATE api_keys
SET requests_this_month = 0,
    last_reset_at = NOW()
WHERE key_prefix = 'gg_live_XXX...';
```

### Fazer Upgrade de Plano

```sql
UPDATE api_keys
SET plan = 'enterprise',
    monthly_quota = NULL,  -- NULL = ilimitado
    requests_this_month = 0,
    last_reset_at = NOW()
WHERE key_prefix = 'gg_live_XXX...';
```

### Revogar uma Key

```sql
UPDATE api_keys
SET is_revoked = true,
    revoked_at = NOW()
WHERE key_prefix = 'gg_live_XXX...';
```

### Listar Todas as Keys Ativas

```sql
SELECT
    key_prefix,
    client_name,
    plan,
    monthly_quota,
    requests_this_month,
    total_requests,
    created_at
FROM api_keys
WHERE is_active = true
  AND is_revoked = false
ORDER BY created_at DESC;
```

### Estatísticas Gerais

```sql
-- Total de keys por plano
SELECT plan, COUNT(*) as total
FROM api_keys
WHERE is_active = true
GROUP BY plan;

-- Total de requisições este mês
SELECT SUM(requests_this_month) as total_requests_month
FROM api_keys;

-- Keys próximas do limite
SELECT
    key_prefix,
    client_name,
    plan,
    requests_this_month,
    monthly_quota,
    ROUND(requests_this_month::numeric / monthly_quota * 100, 2) as percentage_used
FROM api_keys
WHERE monthly_quota IS NOT NULL
  AND requests_this_month::numeric / monthly_quota > 0.8
ORDER BY percentage_used DESC;
```

## Segurança

### Armazenamento Seguro

- ✅ API keys são armazenadas como **hash SHA256** no banco
- ✅ Plaintext só é exibido **uma vez** na criação
- ✅ Prefixo visível (12 primeiros chars) para identificação
- ✅ Não há como "recuperar" uma key perdida (só criar nova)

### Proteção contra Race Conditions

- ✅ **SELECT FOR UPDATE**: Lock pessimista na row
- ✅ **UPDATE atômico**: Incremento direto no SQL
- ✅ **Commit manual**: Lock mantido até commit explícito

### Headers CORS

- ✅ Configurados em todas as respostas (200, 401, 403, 429, 500)
- ✅ Preflight OPTIONS permitido sem validação

### Validação

- ✅ Middleware executa **antes** do endpoint
- ✅ Valida key + verifica quota + incrementa contador
- ✅ Quota checada **com lock** (atomicidade garantida)

## Fluxo de Validação

```
1. Request chega ao servidor
   ↓
2. OPTIONS? → Bypass (preflight CORS)
   ↓
3. Path público? → Bypass
   ↓
4. Extrair header x-api-key
   ↓
5. Sem key? → 403
   ↓
6. SELECT FOR UPDATE (lock pessimista)
   ↓
7. Key inválida? → 401
   ↓
8. Sem quota? → 429
   ↓
9. Incrementar contador (UPDATE atômico sem commit)
   ↓
10. COMMIT (libera lock)
   ↓
11. Processar requisição
   ↓
12. Adicionar headers X-RateLimit-*
   ↓
13. Retornar resposta
```

## Reset Mensal de Quota

O reset acontece automaticamente:

- **Quando**: 30 dias após `last_reset_at`
- **Como**: Ao fazer próxima validação, detecta que passou 30 dias
- **Comportamento**:
  - `requests_this_month` → 1 (conta a request atual)
  - `last_reset_at` → NOW()
  - `total_requests` → incrementado normalmente

## Troubleshooting

### "API Key não fornecida"
- Verifique se o header `x-api-key` está sendo enviado
- Certifique-se que não há espaços antes/depois da key

### "API Key inválida"
- Key pode estar incorreta (typo)
- Key pode ter sido revogada
- Key pode ter expirado (se teve `expires_at` configurado)

### "Quota excedida"
- Verificar `requests_this_month` no banco
- Opções:
  - Aguardar reset mensal (30 dias)
  - Fazer upgrade de plano
  - Resetar manualmente com SQL (apenas para testes)

### Contador não incrementa
- ✅ CORRIGIDO: Bug do path "/" foi removido
- ✅ CORRIGIDO: Race conditions resolvidas com SELECT FOR UPDATE
- ✅ CORRIGIDO: Timezone naive/aware resolvido

### CORS errors
- ✅ CORRIGIDO: Headers CORS em todas as respostas
- ✅ CORRIGIDO: OPTIONS (preflight) permitido sem validação

## Arquivos Importantes

```
backend/
├── app/
│   ├── models/
│   │   └── api_key.py              # Modelo de dados
│   ├── services/
│   │   └── api_key_service.py      # Lógica de negócio
│   ├── middleware/
│   │   └── api_key_tracker.py      # Interceptador de requests
│   ├── api/
│   │   └── admin_api_keys.py       # Endpoints admin
│   └── scripts/
│       └── create_api_key.py       # Script CLI
├── alembic/
│   └── versions/
│       └── 004_api_keys.py         # Migration
└── criar_minha_primeira_key.py     # Script interativo
```

## Changelog

### 2025-12-18 - Sistema Estável ✅

**Bugs críticos corrigidos:**
1. ✅ Path "/" causava bypass em todas as requisições
2. ✅ Race conditions permitiam exceder quota
3. ✅ TypeError: timezone-naive vs timezone-aware
4. ✅ DetachedInstanceError após commit
5. ✅ CORS errors bloqueavam respostas de erro
6. ✅ OPTIONS (preflight) bloqueado por falta de key

**Features implementadas:**
- ✅ 3 planos (Free/Professional/Enterprise)
- ✅ Quota enforcement com lock pessimista
- ✅ Headers informativos de quota
- ✅ Frontend mostrando mensagens corretas
- ✅ Sistema 100% funcional em produção

## Próximos Passos (Opcional)

1. **Dashboard Web**: Interface para gerenciar keys
2. **Webhooks**: Notificar quando quota está acabando
3. **Analytics**: Gráficos de uso por key/plano
4. **Billing**: Integração com gateway de pagamento
5. **API Keys com escopos**: Limitar a endpoints específicos

## Suporte

Para dúvidas ou problemas:
- Verificar logs no Railway
- Consultar tabela `api_keys` no Supabase
- Revisar este documento

---

**Sistema desenvolvido e testado em produção.**
**Status: ✅ FUNCIONANDO**
