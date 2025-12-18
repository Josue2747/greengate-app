# 👉 COMECE AQUI - Setup em 4 Minutos

## ✅ Já está pronto no Railway (automático):
- ✅ Código enviado para GitHub
- ✅ Todas as correções aplicadas
- ✅ Painel admin implementado
- ✅ Dependências instaladas automaticamente

## 🎯 Você só precisa fazer 2 coisas:

### 1. Configurar 3 variáveis no Railway (1 minuto)

**Railway → Variables → Raw Editor → Cole:**

```
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=ce53b6ca5cb2680187918a97b2523d020094f93f50dae61cbb97ae62bf1a0e0a
SECRET_KEY=e01d668e74ff4633041539bbbbb93e098b6e5dc98e23b4203a6d01de266ac42a
```

Clique em **Deploy**. Pronto!

---

### 2. Baixar e usar o painel admin (3 minutos)

**a) Baixar arquivo:**
- `backend/admin-panel.html` → Salvar no seu computador

**b) Editar linha 12:**
```javascript
const API_URL = 'https://SEU-PROJETO.up.railway.app/api/v1';
```
(troque `SEU-PROJETO` pela URL real do Railway)

**c) Abrir no navegador:**
- Duplo clique no arquivo
- Login: `admin`
- Senha: `admin123`

**d) Clicar no botão laranja:**
- **"⚙️ Rodar Migrations (1x)"**
- Confirmar
- Aguardar "Sucesso!"
- (Isso cria índices de performance - só precisa fazer UMA VEZ)

---

## 🎉 PRONTO!

Agora você pode:
- ✅ Criar API Keys para clientes
- ✅ Ver estatísticas de uso
- ✅ Revogar keys
- ✅ Fazer upgrade de planos

---

## 🔑 Criar sua primeira API Key:

1. No painel admin, clique **"➕ Criar Nova API Key"**
2. Preencha:
   - Nome do cliente: `Fazenda Teste`
   - Plano: `Free` (1 validação/mês)
3. Copie a API key (ela só aparece UMA VEZ!)
4. Teste no Postman/Insomnia:

```bash
POST https://SEU-PROJETO.up.railway.app/api/v1/validate/quick
Header: x-api-key: gg_live_xxxxx
Body: {
  "type": "Polygon",
  "coordinates": [...]
}
```

---

## 📚 Mais informações:

- **Guia rápido:** `README-RAPIDO.md`
- **Detalhes:** `ACOES-NECESSARIAS.md`
- **Variáveis prontas:** `RAILWAY-ENV-VARS.txt`
- **Documentação completa:** `ADMIN-PANEL.md`

---

**Tempo total: 4 minutos** ⏱️

**Não precisa de Shell, terminal ou comandos!** 🎉

Tudo pelo painel web admin.
