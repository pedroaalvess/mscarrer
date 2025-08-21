# Microsoft Jobs - Deploy Instructions

## Deploy no Railway

### 1. Preparação
- Certifique-se de que todos os arquivos estão no repositório
- Verifique se o `requirements.txt` está atualizado
- Confirme que o `Procfile` está configurado corretamente

### 2. Deploy
1. Conecte seu repositório ao Railway
2. **IMPORTANTE:** Adicione um banco PostgreSQL no Railway:
   - Vá em "Add Service" → "Database" → "PostgreSQL"
   - Railway criará automaticamente a variável `DATABASE_URL`
3. Configure as variáveis de ambiente:
   - `FLASK_ENV=production`
   - `PORT=5000` (opcional, Railway define automaticamente)
   - `DATABASE_URL` (criada automaticamente pelo PostgreSQL)
4. O deploy será automático após o push

### 3. Persistência de Dados 🔒
- ✅ **Banco PostgreSQL:** Dados permanentes no Railway
- ✅ **SQLite local:** Para desenvolvimento (arquivo `microsoft_jobs.db`)
- ✅ **Backup automático:** Script `backup_restore.py` incluído
- ✅ **Sem perda de dados:** Candidaturas preservadas entre deploys

### 4. Backup e Restore
```bash
# Criar backup
python backup_restore.py backup

# Restaurar backup
python backup_restore.py restore backup_microsoft_jobs_20250820_123456.json
```

### 5. Estrutura do Projeto
```
microsoft_jobs/
├── src/
│   ├── main.py              # Aplicação principal
│   ├── models/              # Modelos do banco de dados
│   ├── routes/              # Rotas da API
│   └── static/              # Arquivos estáticos (HTML, CSS, JS)
├── requirements.txt         # Dependências Python
├── Procfile                # Comando de inicialização
├── railway.json            # Configuração Railway
├── backup_restore.py       # Script de backup/restore
├── microsoft_jobs.db       # Banco SQLite local (desenvolvimento)
└── README_DEPLOY.md        # Este arquivo
```

### 6. Funcionalidades
- ✅ Página de vagas de emprego Microsoft France
- ✅ Formulário de candidatura com upload de documentos
- ✅ Painel administrativo para RH
- ✅ Design responsivo (desktop e mobile)
- ✅ Animação de sucesso no envio
- ✅ Formatação automática de telefone e data
- ✅ **DADOS PERSISTENTES - NÃO APAGAM!**

### 7. Acesso Admin
- URL: `/microsoft-rh-admin-portal`
- Login: `microsoft_hr`
- Senha: `microsoft_hr_2025`

### 8. Tecnologias
- Backend: Flask + SQLAlchemy
- Frontend: HTML5 + CSS3 + JavaScript
- Banco: PostgreSQL (produção) / SQLite (desenvolvimento)
- Deploy: Railway + Gunicorn

### 9. Garantias de Persistência 🛡️
- ✅ Banco PostgreSQL no Railway (permanente)
- ✅ Configuração que preserva dados existentes
- ✅ Não recria tabelas se já existem
- ✅ Script de backup para segurança extra
- ✅ Candidaturas nunca são perdidas

