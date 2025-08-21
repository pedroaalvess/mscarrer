# Site de Vagas de Emprego Microsoft France

## 📋 Descrição do Projeto

Este projeto é uma página completa de vagas de emprego da Microsoft France, desenvolvida em francês, com sistema de candidaturas e painel administrativo. O site foi criado seguindo o design e estilo visual do site oficial da Microsoft.

## ✨ Funcionalidades Principais

### 🎨 Design e Interface
- **Design baseado no site oficial da Microsoft** com cores, tipografia e elementos visuais consistentes
- **Página totalmente em francês** com conteúdo localizado
- **Design responsivo** compatível com desktop e mobile
- **Carrossel de imagens** na seção hero com transições suaves
- **Navegação intuitiva** com menu fixo e links de ancoragem

### 💼 Sistema de Vagas
- **Carrossel de vagas** com navegação por setas
- **Filtros avançados** por departamento, nível de experiência e tipo de contrato
- **6 vagas pré-cadastradas** em diferentes departamentos (Marketing, AI Research, Engineering, Security, Product Management)
- **Informações detalhadas** de cada vaga com localização, departamento e descrição

### 📝 Sistema de Candidaturas
- **Formulário completo** com todos os campos solicitados:
  - Nome e Sobrenome
  - Data de nascimento
  - Nacionalidade
  - Email
  - SPI (opcional)
  - Telefone
  - Endereço
  - Upload de documentos (frente, verso, comprovante de endereço)
- **Validação de arquivos** (PNG, JPG, JPEG, PDF)
- **Armazenamento seguro** dos dados e documentos

### 🔐 Painel Administrativo
- **Acesso protegido por senha**: `microsoft_hr_2025`
- **Dashboard com estatísticas** em tempo real
- **Listagem de candidaturas** com informações resumidas
- **Visualização detalhada** de cada candidatura
- **Download de documentos** enviados pelos candidatos
- **Sistema de status** para acompanhamento das candidaturas

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask** (Python) - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados
- **Flask-CORS** - Suporte a CORS
- **Werkzeug** - Upload de arquivos

### Frontend
- **HTML5** semântico
- **CSS3** com Flexbox e Grid
- **JavaScript** vanilla para interatividade
- **Google Fonts** (Segoe UI)
- **Design responsivo** com media queries

## 📁 Estrutura do Projeto

```
microsoft_jobs/
├── src/
│   ├── models/
│   │   ├── user.py          # Modelo de usuário
│   │   ├── job.py           # Modelo de vagas
│   │   └── application.py   # Modelo de candidaturas
│   ├── routes/
│   │   ├── jobs.py          # Rotas das vagas
│   │   └── admin.py         # Rotas administrativas
│   ├── static/
│   │   ├── images/          # Imagens do site
│   │   ├── uploads/         # Arquivos enviados
│   │   ├── index.html       # Página principal
│   │   ├── styles.css       # Estilos CSS
│   │   └── script.js        # JavaScript
│   ├── database/
│   │   └── app.db          # Banco de dados SQLite
│   └── main.py             # Arquivo principal Flask
├── populate_db.py          # Script para popular banco
├── requirements.txt        # Dependências Python
└── README.md              # Esta documentação
```

## 🚀 Como Executar

### 1. Ativação do Ambiente Virtual
```bash
cd microsoft_jobs
source venv/bin/activate
```

### 2. Instalação de Dependências
```bash
pip install -r requirements.txt
```

### 3. Inicialização do Banco de Dados
```bash
python populate_db.py
```

### 4. Execução do Servidor
```bash
python src/main.py
```

### 5. Acesso ao Site
- **Site principal**: http://localhost:5000
- **Painel administrativo**: Clique em "Espace RH" e use a senha `microsoft_hr_2025`

## 🎯 Funcionalidades Detalhadas

### Página Principal
1. **Header fixo** com navegação e botão de acesso RH
2. **Seção Hero** com carrossel de 3 slides e call-to-actions
3. **Seção "Sobre a empresa"** com 3 cards informativos
4. **Seção "Benefícios"** com 6 benefícios em grid
5. **Seção "Vagas"** com filtros e carrossel de vagas
6. **Rodapé completo** com links organizados em colunas

### Sistema de Candidaturas
1. **Modal de candidatura** que abre ao clicar em "Postuler"
2. **Formulário com validação** de campos obrigatórios
3. **Upload múltiplo** de arquivos com validação de tipo
4. **Feedback visual** com notificações de sucesso/erro
5. **Armazenamento seguro** no servidor

### Painel Administrativo
1. **Login seguro** com autenticação por token
2. **Dashboard** com 4 métricas principais
3. **Lista de candidaturas** com informações resumidas
4. **Detalhes completos** de cada candidatura
5. **Download individual** de documentos
6. **Interface responsiva** e profissional

## 🔒 Segurança

- **Validação de arquivos** por extensão e tipo MIME
- **Nomes únicos** para arquivos enviados (UUID)
- **Autenticação** para área administrativa
- **Sanitização** de dados de entrada
- **Proteção CORS** configurada

## 📱 Responsividade

O site é totalmente responsivo e se adapta a:
- **Desktop** (1200px+)
- **Tablet** (768px - 1199px)
- **Mobile** (até 767px)

## 🎨 Design System

### Cores Principais
- **Azul Microsoft**: #0078D4
- **Azul Hover**: #106EBE
- **Cinza Texto**: #323130
- **Cinza Claro**: #605E5C
- **Fundo Claro**: #F3F2F1

### Tipografia
- **Fonte**: Segoe UI (fonte oficial da Microsoft)
- **Tamanhos**: 48px (H1), 32px (H2), 24px (H3), 20px (H4), 16px (corpo)

### Componentes
- **Botões primários** com hover effects
- **Cards** com sombras sutis
- **Modais** com overlay escuro
- **Formulários** com validação visual

## 📊 Dados de Exemplo

O sistema vem com 6 vagas pré-cadastradas:
1. **Responsable Marketing Digital - Xbox** (Paris, Marketing)
2. **Data Scientist - Intelligence Artificielle** (Grenoble, AI Research)
3. **Développeur Frontend - Teams** (Nantes, Engineering)
4. **Spécialiste Cybersécurité - Defender** (Toulouse, Security)
5. **Chef de Produit - Microsoft 365** (Lyon, Product Management)
6. **Ingénieur Logiciel Senior - Azure** (Paris, Engineering)

## 🔧 Configurações

### Senha Administrativa
- **Senha padrão**: `microsoft_hr_2025`
- **Localização**: `src/routes/admin.py` (variável `ADMIN_SECRET`)

### Upload de Arquivos
- **Tipos permitidos**: PNG, JPG, JPEG, PDF
- **Diretório**: `src/static/uploads/applications/`
- **Nomeação**: UUID único para cada arquivo

### Banco de Dados
- **Tipo**: SQLite
- **Localização**: `src/database/app.db`
- **Modelos**: User, Job, Application

## 🌟 Destaques do Projeto

✅ **Design fiel ao Microsoft** com cores e tipografia oficiais
✅ **Totalmente em francês** conforme solicitado
✅ **Sistema completo de candidaturas** com upload de documentos
✅ **Painel administrativo funcional** com todas as funcionalidades
✅ **Código bem estruturado** e documentado
✅ **Responsivo** para todos os dispositivos
✅ **Seguro** com validações e autenticação
✅ **Pronto para produção** com todas as funcionalidades testadas

## 📞 Suporte

Para dúvidas ou modificações, consulte a documentação do código ou entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido com ❤️ seguindo as especificações da Microsoft France**

