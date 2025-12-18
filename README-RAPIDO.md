# 🚀 Setup Rápido - 2 Passos

## 1️⃣ Configurar Railway (2 min)

### Adicionar Variáveis de Ambiente:

**Railway → Seu Projeto → Variables → Raw Editor**

Cole isto:
```
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=ce53b6ca5cb2680187918a97b2523d020094f93f50dae61cbb97ae62bf1a0e0a
SECRET_KEY=e01d668e74ff4633041539bbbbb93e098b6e5dc98e23b4203a6d01de266ac42a
```

Clique em **"Deploy"** (Railway vai reiniciar automaticamente)

---

## 2️⃣ Usar Painel Admin (2 min)

1. **Baixe** o arquivo `admin-panel.html` para seu computador

2. **Edite** linha 12 com a URL do Railway:
   ```javascript
   const API_URL = 'https://SEU-PROJETO.up.railway.app/api/v1';
   ```

3. **Abra** no navegador e faça login:
   - Username: `admin`
   - Password: `admin123`

4. **⚙️ Rodar Migrations (apenas UMA VEZ):**
   - Clique no botão laranja **"⚙️ Rodar Migrations (1x)"**
   - Confirme
   - Aguarde mensagem de sucesso
   - Isso cria 6 índices de performance no banco

5. **Crie API Keys** para seus clientes!

---

## ✅ Pronto!

Agora você pode:
- ✅ Criar API keys pelo painel admin
- ✅ Validações respeitam quota (Free=1/mês, Pro=50/mês, Enterprise=ilimitado)
- ✅ Sistema 10-50% mais rápido (índices)
- ✅ Todos os bugs corrigidos

---

## 📱 Login Padrão

- **Username:** `admin`
- **Password:** `admin123`

**⚠️ TROCAR EM PRODUÇÃO!**

Para trocar:
```bash
# Local:
cd backend/backend
python -c "from app.core.auth import hash_password; print(hash_password('SuaSenhaForte'))"

# Copie o hash
# Railway → Variables → ADMIN_PASSWORD_HASH → Cole o hash
```

---

## 🆘 Problemas?

- `ACOES-NECESSARIAS.md` - Instruções detalhadas
- `ADMIN-PANEL.md` - Guia completo do painel
- `RAILWAY-ENV-VARS.txt` - Variáveis prontas para copiar

---

**Tempo total: ~4 minutos** ⏱️

**Não precisa de Shell!** Tudo pelo painel admin 🎉
