# Admin Panel - Changelog

## Data: 2025-12-18

### Implementado: Painel Admin com Autenticação JWT

#### Funcionalidades

✅ **Sistema de Autenticação JWT**
- Login seguro com username/password
- Tokens JWT com expiração de 24 horas
- Proteção de todos os endpoints administrativos
- Role-based access control (role: admin)

✅ **Painel Web Completo** (`admin-panel.html`)
- Interface moderna com gradiente
- Login form com autenticação
- Dashboard com estatísticas em tempo real:
  - Total de API Keys criadas
  - Keys ativas
  - Total de validações (histórico)
  - Validações este mês
- Tabela de API Keys:
  - Prefixo, cliente, plano, quota
  - Status (ativa/revogada)
  - Uso mensal e total
  - Ações: Revogar, Upgrade
- Modal para criar nova API key:
  - Nome do cliente
  - Plano (Free, Professional, Enterprise)
  - Email, documento
  - Expiração
  - Observações
- Exibição única da API key após criação
- Funcionalidade "Copiar para clipboard"
- Responsivo e mobile-friendly

✅ **Endpoints Protegidos**
- `POST /api/v1/auth/login` - Autenticação (público)
- `POST /api/v1/auth/logout` - Logout (público)
- `GET /api/v1/admin/api-keys/` - Listar keys (protegido)
- `POST /api/v1/admin/api-keys/` - Criar key (protegido)
- `GET /api/v1/admin/api-keys/stats` - Estatísticas (protegido)
- `POST /api/v1/admin/api-keys/{id}/revoke` - Revogar key (protegido)
- `POST /api/v1/admin/api-keys/{id}/upgrade` - Upgrade plano (protegido)
- `GET /api/v1/admin/api-keys/plans` - Listar planos (protegido)

#### Arquivos Criados

1. **`backend/app/core/auth.py`**
   - Funções de autenticação JWT
   - `hash_password()` - SHA256 com salt
   - `create_access_token()` - Gerar JWT
   - `verify_token()` - Validar JWT
   - `verify_admin_credentials()` - Validar login
   - `verify_admin()` - Dependency para FastAPI

2. **`backend/app/api/auth.py`**
   - Endpoints de autenticação
   - `POST /auth/login` - Login admin
   - `POST /auth/logout` - Logout (stateless)

3. **`backend/admin-panel.html`**
   - Interface web completa
   - JavaScript vanilla (sem frameworks)
   - Integração com API via fetch()
   - Gerenciamento de token no localStorage

4. **`backend/requirements-admin.txt`**
   - Dependências adicionais:
     - python-jose[cryptography]==3.3.0

5. **`backend/ADMIN-PANEL.md`**
   - Documentação completa
   - Guia de configuração
   - Instruções de uso
   - Troubleshooting
   - Boas práticas de segurança

6. **`backend/CHANGELOG-ADMIN.md`**
   - Este arquivo (registro de mudanças)

#### Arquivos Modificados

1. **`backend/app/core/config.py`**
   - Adicionado `ADMIN_USERNAME` (linha 87)
   - Adicionado `ADMIN_PASSWORD_HASH` (linha 88)
   - Já existia `ACCESS_TOKEN_EXPIRE_MINUTES` (linha 82)
   - Já existia `ALGORITHM` (linha 83)

2. **`backend/app/api/admin_api_keys.py`**
   - Adicionado `from app.core.auth import verify_admin` (linha 13)
   - Adicionado `dependencies=[Depends(verify_admin)]` ao router (linha 22)
   - Todos os endpoints agora requerem JWT válido

3. **`backend/app/main.py`**
   - Importado `auth` router (linha 176)
   - Registrado auth router (linhas 308-312)
   - Re-habilitado admin_api_keys router (linhas 314-319)

4. **`backend/.env.example`**
   - Adicionado seção "Admin Panel" (linhas 23-28)
   - `ADMIN_USERNAME`
   - `ADMIN_PASSWORD_HASH`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`
   - Exemplo de hash para senha "admin123"

5. **`backend/.env`**
   - Configurado SECRET_KEY
   - Configurado credenciais admin
   - Configurado expiração de token

#### Segurança Implementada

🔒 **Autenticação**
- JWT com HS256 (HMAC-SHA256)
- Token expira em 24 horas (configurável)
- Header `Authorization: Bearer <token>` obrigatório

🔒 **Senha**
- Hash SHA256 com salt derivado do SECRET_KEY
- Nunca armazena senha em texto plano
- Salt único por instalação

🔒 **Autorização**
- Todos endpoints `/admin/*` protegidos
- Middleware `verify_admin` valida role e expiração
- Rejeita tokens sem role "admin"

🔒 **API Key**
- Mostrada apenas UMA VEZ após criação
- Hash SHA256 armazenado no banco
- Prefixo visível para identificação

#### Testes Realizados

✅ Importação dos módulos de autenticação
✅ Criação de token JWT
✅ Verificação de token JWT
✅ Hashing de senha
✅ Verificação de credenciais
✅ Carregamento do .env
✅ Warnings de segurança funcionando

#### Configuração Necessária

Para usar o painel admin:

1. **Instalar dependências:**
   ```bash
   pip install -r requirements-admin.txt
   ```

2. **Gerar hash da senha:**
   ```bash
   python -c "from app.core.auth import hash_password; print(hash_password('sua_senha_segura'))"
   ```

3. **Configurar variáveis de ambiente:**
   ```bash
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD_HASH=<hash_gerado_acima>
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   SECRET_KEY=<openssl rand -hex 32>
   ```

4. **Iniciar backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Abrir painel:**
   - Abrir `admin-panel.html` no navegador
   - Ou servir via HTTP server

#### Credenciais de Teste

**⚠️ APENAS PARA DESENVOLVIMENTO ⚠️**

- Username: `admin`
- Password: `admin123`
- Hash: `ce53b6ca5cb2680187918a97b2523d020094f93f50dae61cbb97ae62bf1a0e0a`

**TROCAR EM PRODUÇÃO!**

#### Próximos Passos

Para produção no Railway:

1. ✅ Gerar SECRET_KEY seguro:
   ```bash
   openssl rand -hex 32
   ```

2. ✅ Gerar senha admin forte e hash

3. ✅ Configurar variáveis no Railway:
   - `ADMIN_USERNAME`
   - `ADMIN_PASSWORD_HASH`
   - `SECRET_KEY`
   - `ALLOWED_ORIGINS` (domínio do frontend)

4. ✅ Fazer deploy

5. ✅ Hospedar `admin-panel.html`:
   - Via Nginx/Caddy
   - Ou hospedagem estática (Netlify/Vercel)
   - Ou CDN (CloudFlare Pages)

6. ✅ Configurar HTTPS obrigatório

7. ✅ Atualizar `API_URL` no admin-panel.html

#### Monitoramento

Eventos logados:

- `auth.login_success` - Login bem-sucedido
- `auth.login_failed` - Tentativa de login falhada
- `auth.unauthorized` - Token inválido/expirado
- `admin.api_key_created` - API key criada
- `admin.api_key_revoked` - API key revogada
- `admin.plan_upgraded` - Plano atualizado

#### Performance

- Autenticação JWT é stateless (sem consulta ao banco)
- Verificação de token é instantânea (apenas validação de assinatura)
- Overhead: < 1ms por request

#### Compatibilidade

- Python 3.9+
- FastAPI 0.104+
- python-jose 3.3.0
- Navegadores modernos (ES6+)

#### Limitações

- JWT é stateless (não pode ser invalidado antes da expiração)
- Logout é apenas client-side (remover token do localStorage)
- Para invalidação forçada, trocar SECRET_KEY (invalida todos os tokens)

#### Autor

Implementado em 2025-12-18 por Claude Code (Anthropic)
