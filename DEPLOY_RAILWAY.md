# 🚀 Deploy Microsoft Jobs no Railway

## 📋 Instruções Completas de Deploy

### 1. **Preparação do Projeto**
Este ZIP contém todos os arquivos necessários para deploy no Railway:

```
microsoft_jobs/
├── src/                    # Código fonte da aplicação
├── requirements.txt        # Dependências Python
├── Procfile               # Comando de inicialização
├── railway.json           # Configuração Railway
├── .env.example           # Exemplo de variáveis de ambiente
└── README_DEPLOY.md       # Instruções detalhadas
```

### 2. **Deploy no Railway**

#### Passo 1: Criar Projeto
1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo" ou "Empty Project"

#### Passo 2: Upload do Código
1. Se escolheu "Empty Project":
   - Extraia o ZIP
   - Conecte seu repositório GitHub
   - Ou use Railway CLI: `railway login` → `railway link` → `railway up`

#### Passo 3: Configurar Banco PostgreSQL
1. No dashboard do Railway, clique em "Add Service"
2. Selecione "PostgreSQL"
3. Aguarde a criação do banco

#### Passo 4: Configurar Variáveis de Ambiente
O Railway detectará automaticamente as variáveis do PostgreSQL.
Variáveis necessárias (configuradas automaticamente):
- `DATABASE_URL` - URL do PostgreSQL
- `PGHOST` - Host do banco
- `PGPORT` - Porta do banco
- `PGDATABASE` - Nome do banco
- `PGUSER` - Usuário do banco
- `PGPASSWORD` - Senha do banco

### 3. **Configuração Automática**

O projeto está configurado para:
- ✅ **Auto-deploy** quando código é atualizado
- ✅ **Banco PostgreSQL** persistente
- ✅ **Todas as 6 vagas** criadas automaticamente
- ✅ **Upload de arquivos** funcionando
- ✅ **CORS habilitado** para frontend
- ✅ **Gunicorn** como servidor de produção

### 4. **Acesso ao Site**

Após o deploy:
- **Site principal**: `https://seu-projeto.railway.app`
- **Painel admin**: `https://seu-projeto.railway.app/microsoft-rh-admin-portal`
  - Login: `microsoft_hr`
  - Senha: `microsoft_hr_2025`

### 5. **Funcionalidades Incluídas**

#### 🎯 **Site Completo**
- ✅ Design Microsoft oficial
- ✅ 6 vagas de emprego em francês
- ✅ Carrossel de vagas responsivo
- ✅ Formulário de candidatura completo
- ✅ Upload de documentos (ID + comprovante)
- ✅ Animação de sucesso
- ✅ Formatação automática (telefone + data)

#### 🔐 **Painel Administrativo**
- ✅ Login seguro para RH
- ✅ Lista de todas as candidaturas
- ✅ Visualização completa dos dados
- ✅ Download de documentos
- ✅ Interface responsiva

#### 📱 **Mobile Otimizado**
- ✅ Formulário funciona perfeitamente no mobile
- ✅ Design responsivo
- ✅ Touch events otimizados
- ✅ Animações suaves

### 6. **Estrutura do Banco de Dados**

O sistema cria automaticamente:
- **Tabela Jobs**: 6 vagas pré-cadastradas
- **Tabela Applications**: Candidaturas dos usuários
- **Upload de arquivos**: Documentos organizados por candidatura

### 7. **Monitoramento**

No Railway você pode:
- Ver logs em tempo real
- Monitorar uso de recursos
- Configurar domínio customizado
- Escalar automaticamente

### 8. **Suporte**

Em caso de problemas:
1. Verifique os logs no Railway
2. Confirme que PostgreSQL está rodando
3. Verifique se todas as variáveis estão configuradas
4. Teste a conexão com o banco

---

## 🎉 **Pronto para Produção!**

Este projeto está 100% configurado e testado para produção no Railway.
Todas as funcionalidades foram validadas e estão funcionando perfeitamente.

**Boa sorte com seu deploy! 🚀**

