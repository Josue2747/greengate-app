# Painel Admin - GreenGate

## Visão Geral

Painel web seguro para gerenciar API Keys do GreenGate, protegido por autenticação JWT.

## Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements-admin.txt
```

### 2. Configurar Credenciais

#### Gerar Hash da Senha

```bash
python -c "from app.core.auth import hash_password; print(hash_password('sua_senha_segura'))"
```

#### Configurar Variáveis de Ambiente

No Railway ou arquivo `.env`:

```bash
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=<hash_gerado_acima>
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 horas
```

**Exemplo** (senha: `admin123`):
```bash
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=ce53b6ca5cb2680187918a97b2523d020094f93f50dae61cbb97ae62bf1a0e0a
```

⚠️ **TROCAR SENHA EM PRODUÇÃO!**

### 3. Iniciar Backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 4. Abrir Painel Admin

Abra `admin-panel.html` no navegador ou sirva via servidor web:

```bash
# Opção 1: Abrir diretamente
open admin-panel.html

# Opção 2: Servir via Python
python -m http.server 8080
# Acessar: http://localhost:8080/admin-panel.html
```

## Uso

### Login

1. Acesse o painel admin
2. Entre com:
   - Username: `admin` (ou valor de `ADMIN_USERNAME`)
   - Password: sua senha configurada
3. O token JWT é armazenado automaticamente no `localStorage`

### Criar API Key

1. Clique em "Criar Nova API Key"
2. Preencha:
   - **Nome do Cliente**: Nome/empresa (obrigatório)
   - **Plano**: Free (1/mês), Professional (50/mês) ou Enterprise (ilimitado)
   - **Email**: Email do cliente (opcional)
   - **Documento**: CNPJ/CPF (opcional)
   - **Expira em (dias)**: Deixe vazio para nunca expirar
   - **Observações**: Notas internas (opcional)
3. Clique em "Criar Key"
4. **IMPORTANTE**: A API Key é mostrada UMA ÚNICA VEZ
   - Copie e envie para o cliente
   - Ela não será mostrada novamente

### Gerenciar Keys

- **Visualizar**: Tabela mostra todas as keys com status e uso
- **Filtrar**: Use os filtros por plano ou status
- **Revogar**: Clique em "Revogar" para desativar uma key
- **Upgrade**: Clique em "Upgrade" para mudar o plano

### Estatísticas

Dashboard mostra:
- Total de API Keys criadas
- Keys ativas
- Total de validações (histórico)
- Validações este mês
- Distribuição por plano

## Segurança

### Proteção Implementada

✅ **Autenticação JWT**
- Token Bearer com expiração de 24 horas
- Role-based access control (apenas role `admin`)

✅ **Senha Hasheada**
- SHA256 com salt derivado do `SECRET_KEY`
- Nunca armazena senha em texto plano

✅ **Endpoints Protegidos**
- Todos os endpoints `/api/v1/admin/*` requerem JWT válido
- Middleware `verify_admin` valida role e expiração

✅ **API Key Mostrada Uma Vez**
- Após criação, key nunca é mostrada novamente
- Apenas prefixo visível na listagem

### Boas Práticas

1. **TROCAR SENHA PADRÃO** em produção
2. **Usar HTTPS** em produção (não servir admin-panel via HTTP)
3. **Rotacionar SECRET_KEY** periodicamente
4. **Limitar IPs** que podem acessar admin (via firewall/reverse proxy)
5. **Monitorar Logs** de autenticação falhada

## API Endpoints

### Autenticação

#### POST `/api/v1/auth/login`

**Request**:
```json
{
  "username": "admin",
  "password": "sua_senha"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### Admin - API Keys (Protegidos)

Todos os endpoints abaixo requerem header:
```
Authorization: Bearer <token_jwt>
```

#### POST `/api/v1/admin/api-keys/`
Cria nova API Key.

#### GET `/api/v1/admin/api-keys/`
Lista todas as keys (com filtros).

#### GET `/api/v1/admin/api-keys/stats`
Estatísticas de uso.

#### POST `/api/v1/admin/api-keys/{id}/revoke`
Revoga uma key (soft delete).

#### POST `/api/v1/admin/api-keys/{id}/upgrade`
Faz upgrade/downgrade de plano.

#### GET `/api/v1/admin/api-keys/plans`
Retorna planos disponíveis.

## Troubleshooting

### Erro: "Credenciais inválidas"

- Verificar `ADMIN_USERNAME` e `ADMIN_PASSWORD_HASH` no `.env`
- Regenerar hash da senha:
  ```bash
  python -c "from app.core.auth import hash_password; print(hash_password('senha'))"
  ```

### Erro: "Token expirado"

- Token expira após 24 horas por padrão
- Faça login novamente
- Ajuste `ACCESS_TOKEN_EXPIRE_MINUTES` se necessário

### Erro: "CORS blocked"

- Configurar `ALLOWED_ORIGINS` no `.env`
- Ou servir admin-panel no mesmo domínio do backend

### Erro 500 ao criar key

- Verificar logs do backend
- Garantir que `SECRET_KEY` está configurado
- Verificar conexão com banco de dados

## Logs

Eventos importantes são registrados:

```log
# Login bem-sucedido
auth.login_success username=admin

# Tentativa de login falhada
auth.login_failed username=admin

# API Key criada
admin.api_key_created key_prefix=gg_live_abc... client=Fazenda XYZ

# Token inválido
auth.unauthorized error=Token expired
```

## Desenvolvimento

Para desenvolvimento local:

```bash
# Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (admin-panel.html)
# Editar linha 12 para apontar para backend local:
const API_URL = 'http://localhost:8000/api/v1';
```

## Produção

Para produção no Railway:

1. Configurar variáveis de ambiente no Railway:
   ```
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD_HASH=<hash_seguro>
   SECRET_KEY=<openssl rand -hex 32>
   ALLOWED_ORIGINS=https://seu-dominio.com
   ```

2. Fazer deploy do backend

3. Hospedar `admin-panel.html`:
   - **Opção A**: Servir via Nginx/Caddy junto com API
   - **Opção B**: Hospedagem estática (Netlify/Vercel)
   - **Opção C**: CDN (CloudFlare Pages)

4. Atualizar `API_URL` no admin-panel.html:
   ```javascript
   const API_URL = 'https://api.greengate.com.br/api/v1';
   ```

5. **IMPORTANTE**: Servir via HTTPS obrigatoriamente

## Monitoramento

Endpoints úteis para monitorar o sistema:

- `GET /health` - Status básico
- `GET /health/detailed` - Status detalhado + métricas de pool
- `GET /metrics` - Métricas de CPU/memória

## Suporte

Para problemas ou dúvidas, consulte:

- Documentação da API: `/docs`
- Logs do servidor: `journalctl -u greengate -f` (systemd)
- Logs do Railway: Dashboard → Logs
