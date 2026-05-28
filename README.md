# 📋 Sistema de Gestão de Convênios — UESPI

> Aplicação desktop para gerenciamento de convênios de estágio da Universidade Estadual do Piauí (UESPI), com painéis distintos por perfil de acesso, geração de documentos e controle de vencimentos.

## ✨ Funcionalidades

| Funcionalidade | Perfil |
|---|---|
| Login com autenticação por perfil (gestor / empresa) | Ambos |
| Painel do gestor com visão geral dos convênios | Gestor |
| Painel da empresa com convênios próprios | Empresa |
| Solicitação de novos convênios | Empresa |
| Aprovação / cancelamento de convênios | Gestor |
| Edição de convênios com registro de alterações | Gestor |
| Alertas de convênios próximos ao vencimento | Gestor |
| Histórico de convênios encerrados e cancelados | Ambos |
| Geração de PDF do Termo de Abertura | Gestor |
| Notificações internas no sistema | Ambos |

## 🛠️ Tecnologias Utilizadas

- **[Python 3.12](https://www.python.org/)** — linguagem base
- **[Flet 0.85](https://flet.dev/)** — interface gráfica desktop (baseada em Flutter)
- **[Flask 3.1](https://flask.palletsprojects.com/)** — API REST backend
- **[SQLAlchemy 2.0](https://www.sqlalchemy.org/)** — ORM
- **[MySQL](https://www.mysql.com/)** — banco de dados relacional
- **[ReportLab](https://www.reportlab.com/)** + **[python-docx](https://python-docx.readthedocs.io/)** — geração de PDF e documentos Word
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — gerenciamento de variáveis de ambiente

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python **3.12+**
- MySQL **8.0+** em execução local
- `pip` (gerenciador de pacotes Python)
- `git`

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/sistema-convenios.git
cd sistema-convenios
```

### 2. Crie e ative o ambiente virtual

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```
### 4. Crie o banco de dados

No MySQL, execute o script de criação das tabelas:

```bash
mysql -u root -p < database/scripts.sql
```
### 5. Execute a aplicação

```bash
python run.py
```

O sistema aplicará migrações automáticas e abrirá a interface desktop.

## 🗄️ Modelo de Dados

```
empresas
  id, nome, cnpj, email, telefone, endereco

usuarios
  id, nome, email, senha (hash), perfil (empresa|gestor|admin), empresa_id → empresas

convenios
  id, empresa_id → empresas
  nome, descricao, tipo_convenio (obrigatorio|nao_obrigatorio|supervisionado)
  data_inicio, data_fim, status (ativo|pendente|cancelado)
  responsavel_legal, cnpj, telefone, endereco
  documento_anexo, arquivo_documento
  aprovado_por, data_aprovacao
  motivo_cancelamento, data_cancelamento
  motivo_alteracao, campos_alterados, alterado_em   ← auditoria
  deletado, excluido_em, motivo_exclusao             ← soft delete
```
## 👤 Perfis de Acesso

### Gestor (UESPI)
- Visualiza todos os convênios cadastrados
- Aprova, edita ou cancela convênios
- Recebe alertas de vencimentos próximos (< 30 dias)
- Gera documentos PDF do Termo de Abertura
- Consulta o histórico completo com auditoria de alterações

### Empresa Conveniada
- Solicita novos convênios diretamente pelo sistema
- Acompanha o status dos seus convênios
- Recebe notificações sobre aprovações e vencimentos

## 🔐 Segurança

- Senhas armazenadas com hash via **Werkzeug** (`generate_password_hash`)
- Autenticação por sessão com verificação de perfil em cada rota
- Soft delete: convênios removidos não são apagados do banco, apenas marcados como `deletado = True`
- Registro de auditoria em cada edição: campos alterados, motivo e timestamp

## 📄 Geração de Documentos

O sistema gera automaticamente o **Termo de Abertura de Convênio** em PDF a partir de um template `.docx` (`templates/termo_abertura_modelo.docx`), preenchido com os dados do convênio selecionado. As bibliotecas utilizadas são:

- `python-docx` — leitura e preenchimento do template Word
- `ReportLab` / `PyMuPDF` — conversão e exportação para PDF


## Etrutura do Projeto
```text
sistema-convenios/
│
├── backend/
│   ├── __init__.py
│   ├── app.py                         # Inicialização do Flask
│   ├── config.py                      # Configurações globais
│   ├── database.py                    # Configuração/conexão do banco
│   │
│   ├── criar_tabela.py                # Criação inicial das tabelas
│   ├── criar_usuario.py               # Script de criação de usuários
│   ├── criar_empresa_usuario.py       # Relacionamento empresa/usuário
│   ├── criar_modelo_doc.py            # Criação de modelos de documentos
│   │
│   ├── models/                        # Modelos das entidades
│   │   ├── __init__.py
│   │   ├── usuario.py                 # Modelo de usuários
│   │   ├── empresa.py                 # Modelo das empresas
│   │   ├── convenio.py                # Modelo dos convênios
│   │   └── notifications.py           # Modelo de notificações
│   │
│   ├── routes/                        # Rotas/endpoints da API
│   │   ├── __init__.py
│   │   ├── auth.py                    # Rotas de autenticação
│   │   ├── empresas.py                # Rotas das empresas
│   │   ├── convenios.py               # Rotas dos convênios
│   │   ├── dashboard.py               # Rotas do dashboard
│   │   └── notifications.py           # Rotas de notificações
│   │
│   ├── services/                      # Regras de negócio
│   │   ├── __init__.py
│   │   ├── auth_service.py            # Lógica de autenticação
│   │   ├── convenio_service.py        # Regras dos convênios
│   │   ├── vencimento_service.py      # Controle de vencimentos
│   │   ├── notificacao_service.py     # Sistema de notificações
│   │   └── pdf_service.py             # Geração de PDFs/documentos
│   │
│   └── utils/                         # Funções auxiliares
│       ├── __init__.py
│       └── helpers.py
│
├── frontend/                          # Interface gráfica em Flet
│   ├── __init__.py
│   ├── main.py                        # Inicialização da interface
│   │
│   ├── views/                         # Telas do sistema
│   │   ├── __init__.py
│   │   ├── login.py
│   │   ├── convenios.py
│   │   ├── editar_convenio.py
│   │   ├── historico.py
│   │   ├── notificacoes.py
│   │   ├── painel_empresa.py
│   │   ├── painel_gestor.py
│   │   ├── proximos_vencimento.py
│   │   └── solicitar_novo_convenio.py
│   │
│   └── components/                    # Componentes reutilizáveis
│       ├── __init__.py
│       └── cards.py
│
├── database/
│   ├── scripts.sql                    # Estrutura do banco
│   └── seed.sql                       # Dados iniciais/testes
│
├── templates/                         # Modelos de documentos
│   └── termo_abertura_modelo.docx
│
├── uploads/                           # Arquivos enviados
│   ├── documentos/
│   │ 
│   │
│   └── termos_gerados/                 # PDFs gerados automaticamente
│       ├── termo_24.pdf
│       └── termo_27.pdf
│
├── assets/                            # Recursos visuais do sistema
│   └── brasao_uespi.png
│
├── .git/                              # Controle de versão Git
├── .gitignore
├── README.md
├── requirements.txt
│
├── run.py                             # Inicialização principal
├── seed.py                            # Popular banco com dados iniciais
├── seed_test_notifications.py         # Popular notificações de teste
└── teste_login.py                     # Teste rápido de autenticação
```
## Arquitetura do Projeto
