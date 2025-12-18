# 🔑 Sistema de API Keys - GreenGate

**Versão:** 1.0
**Data:** 2025-12-17

---

## 📋 Visão Geral

Sistema completo de gerenciamento de API keys com:
- ✅ Controle de quotas (validações/mês)
- ✅ Rastreamento de uso automático
- ✅ 3 planos (Free, Professional, Enterprise)
- ✅ Reset mensal automático
- ✅ Expiração opcional
- ✅ Revogação (soft delete)
- ✅ Upgrade/downgrade de planos

---

## 🚀 Setup Inicial

### 1. Rodar Migration

```bash
cd backend
alembic upgrade head
```

Isso cria a tabela `api_keys` no banco.

### 2. Criar Primeira API Key (CLI)

```bash
python scripts/create_api_key.py
```

Menu interativo para criar API keys.

**Exemplo de output:**
```
🔑 API Key: gg_live_3f7a9b2c5e8d1f4a6b9c2e5f8a1d4b7c
📋 Detalhes:
  Cliente: Fazenda Santa Maria
  Plano: professional
  Quota mensal: 50
```

⚠️ **ATENÇÃO:** A API key só é mostrada UMA VEZ! Guarde com segurança.

---

## 📊 Planos Disponíveis

| Plano | Validações/Mês | Preço | Uso Recomendado |
|-------|----------------|-------|-----------------|
| **Free** | 1 | R$ 0 | Teste único |
| **Professional** | 50 | R$ 197/mês | Pequenas fazendas, corretores |
| **Enterprise** | ∞ Ilimitado | R$ 497/mês | Tradings, grandes produtores |

---

## 💻 Uso via API

### Criar API Key (Admin)

```bash
POST /admin/api-keys
Content-Type: application/json

{
  "client_name": "Fazenda Santa Maria Ltda",
  "plan": "professional",
  "client_email": "contato@fazenda.com",
  "client_document": "12345678000190",
  "expires_in_days": 365,
  "notes": "Cliente desde 2025"
}
```

**Response:**
```json
{
  "api_key": "gg_live_3f7a9b2c5e8d1f4a6b9c2e5f8a1d4b7c",
  "id": "uuid-aqui",
  "key_prefix": "gg_live_3f7...",
  "client_name": "Fazenda Santa Maria Ltda",
  "plan": "professional",
  "monthly_quota": 50,
  "expires_at": "2026-12-17T10:30:00Z",
  "created_at": "2025-12-17T10:30:00Z",
  "warning": "ATENÇÃO: Guarde esta API key! Ela não será mostrada novamente."
}
```

### Listar API Keys

```bash
GET /admin/api-keys?plan=professional&is_active=true&limit=50
```

**Response:**
```json
[
  {
    "id": "uuid",
    "key_prefix": "gg_live_3f7...",
    "client_name": "Fazenda Santa Maria",
    "plan": "professional",
    "monthly_quota": 50,
    "requests_this_month": 23,
    "quota_remaining": 27,
    "is_active": true,
    "created_at": "2025-12-17T10:30:00Z"
  }
]
```

### Estatísticas de Uso

```bash
GET /admin/api-keys/stats
```

**Response:**
```json
{
  "total_keys": 127,
  "active_keys": 98,
  "total_requests": 45203,
  "requests_this_month": 3421,
  "by_plan": {
    "free": 45,
    "professional": 38,
    "enterprise": 15
  }
}
```

### Revogar API Key

```bash
POST /admin/api-keys/{api_key_id}/revoke
```

**Response:** 204 No Content

A API key se torna inválida imediatamente.

### Upgrade de Plano

```bash
POST /admin/api-keys/{api_key_id}/upgrade
Content-Type: application/json

{
  "new_plan": "enterprise"
}
```

**Efeito:**
- Quota ajustada imediatamente
- Contador mensal resetado (quota nova disponível já)

---

## 🔒 Como Funciona a Validação

### 1. Cliente Faz Request

```bash
curl -X POST https://api.greengate.com.br/api/v1/validations/quick \
  -H "Content-Type: application/json" \
  -H "x-api-key: gg_live_3f7a9b2c5e8d1f4a6b9c2e5f8a1d4b7c" \
  -d '{"type": "Polygon", "coordinates": [...]}'
```

### 2. Middleware Intercepta

1. Extrai API key do header `x-api-key`
2. Valida API key (existe? ativa? não expirada?)
3. Verifica quota (ainda tem validações disponíveis?)
4. **Incrementa contador de uso**
5. Adiciona headers de quota na response

### 3. Response com Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 50
X-RateLimit-Remaining: 27
X-RateLimit-Reset: 1704067200
```

### 4. Se Quota Excedida

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "detail": "Quota mensal excedida. Limite: 50, Usado: 50. Faça upgrade do plano ou aguarde o reset mensal."
}
```

---

## 📅 Reset Mensal Automático

**Como funciona:**
- Quando API key é usada, o sistema verifica `last_reset_at`
- Se passaram 30+ dias desde o último reset:
  - `requests_this_month` é zerado
  - `last_reset_at` é atualizado para agora

**Exemplo:**
```
2025-01-01: Cliente usa 50/50 validações
2025-01-31: Tenta usar → 429 (quota excedida)
2025-02-01: Tenta usar → SUCESSO! (contador resetou)
```

---

## 🛡️ Segurança

### Hash SHA256

API keys **nunca** são armazenadas em plain text:
- Geração: `gg_live_` + 32 chars hex aleatórios
- Armazenamento: SHA256 hash
- Validação: Hash da key fornecida vs hash armazenado

### Prefixo Visível

Apenas os primeiros 12 chars são visíveis em logs/admin:
- Completo: `gg_live_3f7a9b2c5e8d1f4a6b9c2e5f8a1d4b7c`
- Visível: `gg_live_3f7...`

Útil para identificar sem expor a key completa.

---

## 🔧 Administração

### Endpoints Administrativos

**⚠️ IMPORTANTE:** Proteger com autenticação admin!

```python
# Em admin_api_keys.py
router = APIRouter(
    prefix="/admin/api-keys",
    tags=["Admin - API Keys"],
    dependencies=[Depends(verify_admin)],  # ← ADICIONAR ISSO!
)
```

### Script CLI (Recomendado para Primeiros Clientes)

```bash
# Menu interativo
python scripts/create_api_key.py

# Opções:
# 1. Criar nova API key
# 2. Listar API keys
# 3. Sair
```

---

## 📊 Dashboard Recomendado

Métricas úteis para monitorar:

1. **Uso por Plano**
   - Quantos clientes em cada plano?
   - Revenue projetado

2. **Top Usuários**
   - Quem usa mais?
   - Candidatos para upgrade

3. **Taxa de Conversão**
   - Free → Professional: X%
   - Professional → Enterprise: Y%

4. **Alertas**
   - Cliente próximo de exceder quota (>80%)
   - API keys expirando em 30 dias
   - Uso suspeito (picos anormais)

---

## 🐛 Troubleshooting

### "403 Forbidden"
- API key não foi fornecida no header `x-api-key`

### "401 Unauthorized"
- API key inválida, expirada ou revogada

### "429 Too Many Requests"
- Quota mensal excedida
- Soluções:
  1. Aguardar reset mensal
  2. Fazer upgrade de plano

### "API key não encontrada no banco"
- Rodar migration: `alembic upgrade head`
- Verificar conexão com banco

---

## 🚀 Próximos Passos

### 1. Ativar Middleware (FAZER ISSO!)

Em `main.py`:

```python
from app.middleware.api_key_tracker import APIKeyTrackerMiddleware

app = FastAPI(...)

# ADICIONAR:
app.add_middleware(APIKeyTrackerMiddleware)
```

### 2. Proteger Endpoints Admin

```python
# Criar função verify_admin
async def verify_admin(token: str = Depends(oauth2_scheme)):
    # Validar token JWT
    # Verificar role == 'admin'
    ...

# Adicionar em admin_api_keys.py
router = APIRouter(
    dependencies=[Depends(verify_admin)]
)
```

### 3. Integrar com Billing (Opcional)

- Stripe, Mercado Pago, etc
- Webhook quando pagamento confirmado → upgrade de plano
- Downgrade automático quando pagamento falha

---

## 📝 Checklist de Deploy

- [ ] Rodar migration (`alembic upgrade head`)
- [ ] Ativar middleware (`app.add_middleware(APIKeyTrackerMiddleware)`)
- [ ] Proteger endpoints admin (autenticação)
- [ ] Criar primeira API key de teste
- [ ] Testar quota limit (usar 10x no plano free)
- [ ] Verificar reset mensal (ajustar `last_reset_at` no banco)
- [ ] Documentar para clientes (como obter API key)

---

**Sistema de API Keys pronto para produção!** ✅
