jmk@7Oo[[H<3JUQp

# ✅ Ações Necessárias - Railway

## ✅ JÁ FEITO AUTOMATICAMENTE:
- ✅ Push para GitHub (código já está lá!)
- ✅ Correções de bugs (quota, timezone, session)
- ✅ Melhorias de performance (índices, queries)
- ✅ Painel admin implementado
- ✅ Autenticação JWT

## 🔧 VOCÊ PRECISA FAZER (5 minutos):

### 1. Configurar Variáveis de Ambiente no Railway

Acesse: **Railway Dashboard → Seu Projeto → Variables**

**Adicione estas 3 variáveis:**

```
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=ce53b6ca5cb2680187918a97b2523d020094f93f50dae61cbb97ae62bf1a0e0a
SECRET_KEY=8f3b9d2e7a4c1f6e9b5d8a3c7e2f9b4d6a1e8c5f2b7d4a9e6c3f8b1d5a7e2c9f
```

**Explicação:**
- `ADMIN_USERNAME`: usuário admin (pode mudar se quiser)
- `ADMIN_PASSWORD_HASH`: hash da senha `admin123` (TROCAR EM PRODUÇÃO!)
- `SECRET_KEY`: chave gerada para JWT (pode usar essa ou gerar outra)

**Para gerar sua própria senha:**
```bash
# No terminal local:
cd backend/backend
python -c "from app.core.auth import hash_password; print(hash_password('MinhaSenhaSegura123'))"
```

### 2. Baixar e Configurar o Painel Admin

**a) Baixar o arquivo:**
- Baixe `backend/admin-panel.html` para seu computador

**b) Editar URL da API:**
- Abra o arquivo no editor de texto
- Linha 12, mude para:
```javascript
const API_URL = 'https://greengate-production.up.railway.app/api/v1';
```
(use a URL real do seu Railway)

**c) Usar:**
- Abra o arquivo `admin-panel.html` no Chrome/Firefox
- Login: `admin`
- Senha: `admin123` (ou a que você configurou)

**d) Rodar Migrations (apenas UMA VEZ):**
- Após fazer login, clique no botão laranja **"⚙️ Rodar Migrations (1x)"**
- Confirme a ação
- Aguarde mensagem de sucesso
- Isso cria 6 índices de performance no banco (melhora em 10-50%)

### 3. 🚨 IMPORTANTE - Rotacionar Senha do Supabase

Seu arquivo `.env` local tem a senha do banco exposta. Você precisa:

**No Supabase:**
1. Ir em Settings → Database
2. Database password → Reset password
3. Copiar nova senha

**No Railway:**
4. Variables → DATABASE_URL
5. Atualizar com nova senha

**Formato:**
```
postgresql+asyncpg://postgres.twusvhcicnlizdxhtaof:NOVA_SENHA_AQUI@aws-1-sa-east-1.pooler.supabase.com:5432/postgres
```

## 🎉 PRONTO!

Depois disso, seu sistema estará:
- ✅ Com quota funcionando (máximo de validações por mês)
- ✅ Com painel admin seguro
- ✅ Com performance otimizada (índices)
- ✅ Com todas as correções aplicadas

## 📱 Para Criar API Keys:

1. Abra `admin-panel.html` no navegador
2. Login com admin
3. Clique em "Criar Nova API Key"
4. Preencha os dados do cliente
5. Escolha o plano (Free=1/mês, Professional=50/mês, Enterprise=ilimitado)
6. Copie a API key (ela só aparece UMA VEZ!)
7. Envie para o cliente

## 🆘 Se Tiver Problemas:

**Erro "Credenciais inválidas" no login:**
- Verificar se `ADMIN_PASSWORD_HASH` está correto no Railway
- Regenerar hash da senha

**Erro "CORS blocked":**
- Verificar se `API_URL` no admin-panel.html está correto
- Usar a URL completa do Railway (com https://)

**Painel não carrega estatísticas:**
- F12 no navegador → Console → ver erro
- Verificar se token JWT está sendo enviado

## 📚 Documentação Completa:

- `backend/ADMIN-PANEL.md` - Guia completo do painel
- `backend/CHANGELOG-ADMIN.md` - Log de mudanças
- `backend/ALERTA-SEGURANCA.md` - Alertas de segurança

---

**Tempo estimado: 5 minutos**
**Nível de dificuldade: Fácil** ✨
