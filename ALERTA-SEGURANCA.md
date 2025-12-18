# ⚠️ ALERTA DE SEGURANÇA - AÇÃO NECESSÁRIA

## 🔴 CREDENCIAIS EXPOSTAS NO ARQUIVO .env

**Data**: 2025-12-18
**Severidade**: **CRÍTICA**
**Status**: Aguardando ação do usuário

---

## 📋 PROBLEMA IDENTIFICADO

Durante análise de segurança, foi detectado que o arquivo `.env` contém **credenciais reais do Supabase** em plaintext:

```
DATABASE_URL=postgresql+asyncpg://postgres.twusvhcicnlizdxhtaof:cYSsOyzU1wwgvVps@aws-1-sa-east-1.pooler.supabase.com:5432/postgres
```

**Componentes expostos:**
- Username: `postgres.twusvhcicnlizdxhtaof`
- Password: `cYSsOyzU1wwgvVps`
- Host: `aws-1-sa-east-1.pooler.supabase.com`
- Database: `postgres`

---

## 🎯 AÇÃO IMEDIATA REQUERIDA

### 1. Rotacionar Senha do Banco (URGENTE)

**No Supabase Dashboard:**

1. Acesse https://supabase.com/dashboard
2. Selecione o projeto `twusvhcicnlizdxhtaof`
3. Vá em **Settings** → **Database**
4. Clique em **Reset Database Password**
5. Copie a nova senha gerada

### 2. Atualizar Variáveis de Ambiente no Railway

**No Railway Dashboard:**

1. Acesse https://railway.app
2. Selecione o projeto GreenGate
3. Vá em **Variables**
4. Atualize `DATABASE_URL` com a nova senha:
   ```
   postgresql+asyncpg://postgres.twusvhcicnlizdxhtaof:NOVA_SENHA_AQUI@aws-1-sa-east-1.pooler.supabase.com:5432/postgres
   ```
5. Clique em **Update** → Railway fará redeploy automático

### 3. Atualizar .env Local

**No seu computador:**

1. Edite `backend/.env`
2. Substitua a senha antiga pela nova
3. **NÃO COMMITE** o arquivo .env
4. Verifique se `.env` está no `.gitignore` (já está)

### 4. Gerar SECRET_KEY Segura (RECOMENDADO)

```bash
# Gerar nova chave
openssl rand -hex 32

# Adicionar no Railway (Variables)
SECRET_KEY=<chave_gerada>

# Adicionar no .env local
SECRET_KEY=<chave_gerada>
```

---

## ✅ VERIFICAÇÕES DE SEGURANÇA IMPLEMENTADAS

Para prevenir problemas futuros, as seguintes melhorias foram aplicadas:

### 1. Arquivo .env.example Atualizado
- ✅ Criado com valores de exemplo (sem secrets)
- ✅ Instruções claras de uso
- ✅ Avisos de segurança destacados

### 2. Validação no Startup
- ✅ Sistema verifica se `SECRET_KEY` é padrão
- ✅ Bloqueia startup em produção se não configurada
- ✅ Aviso em desenvolvimento

### 3. Documentação
- ✅ `.env.example` serve como template
- ✅ Nunca commitado com valores reais
- ✅ `.gitignore` protege `.env`

---

## 📖 BOAS PRÁTICAS IMPLEMENTADAS

### Proteção de Secrets

```bash
# ✅ BOM - Usar .env.example como template
cp .env.example .env
# Editar .env com valores reais
# .env está no .gitignore

# ❌ RUIM - Commitar .env com secrets
git add .env
git commit -m "Add configuration"  # NUNCA FAZER ISSO!
```

### Variáveis de Ambiente

```bash
# Desenvolvimento (.env local)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/db
SECRET_KEY=generated-with-openssl-rand-hex-32

# Produção (Railway Variables)
DATABASE_URL=<supabase_connection_string>
SECRET_KEY=<random_secret_key>
ALLOWED_ORIGINS=https://greengate.com.br,https://www.greengate.com.br
```

---

## 🔒 VERIFICAÇÃO DE CONFORMIDADE

Após executar as ações acima, verifique:

- [ ] Senha do Supabase rotacionada
- [ ] `DATABASE_URL` atualizada no Railway
- [ ] `DATABASE_URL` atualizada no `.env` local
- [ ] `SECRET_KEY` gerada e configurada
- [ ] Sistema iniciando sem erros
- [ ] Validações funcionando normalmente
- [ ] `.env` **NÃO** está no git: `git ls-files | grep .env` (deve retornar vazio)

---

## 📞 SUPORTE

Se tiver dúvidas sobre rotação de credenciais:

- **Supabase**: https://supabase.com/docs/guides/database/managing-passwords
- **Railway**: https://docs.railway.app/develop/variables

---

## 📝 HISTÓRICO

- **2025-12-18 08:15**: Credenciais detectadas durante análise de segurança
- **2025-12-18 08:20**: `.env.example` atualizado, validação de startup implementada
- **2025-12-18 08:20**: Aguardando ação do usuário para rotação de senha

---

**⚠️ Até que as credenciais sejam rotacionadas, o banco de dados está potencialmente em risco.**

**Prioridade**: **CRÍTICA** - Executar o mais rápido possível
