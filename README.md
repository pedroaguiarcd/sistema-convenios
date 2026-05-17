# Sistema Convênios
Aplicação para o gerenciamento de convênios de estagios da UESPI.

## Tecnologias
- Python
- Flask (API backend)
- MySQL (banco de dados)
- Flet (interface gráfica)

## Etrutura do Projeto
```text
sistema-convenios/
│
├── backend/
│   ├── app.py                 # Inicialização do Flask
│   ├── database.py            # Conexão e setup do MySQL
│   ├── config.py              # Configurações globais
│   │
│   ├── models/                # Modelos das entidades do sistema
│   │   ├── __init__.py
│   │   ├── usuario.py         # Modelo de usuários
│   │   ├── empresa.py         # Modelo das empresas conveniadas
│   │   ├── convenio.py        # Modelo dos convênios
│   │   └── dashboard.py       # Consultas/resumos do dashboard
│   │
│   ├── routes/                # Rotas/endpoints da API
│   │   ├── __init__.py
│   │   ├── auth.py            # Rotas de autenticação
│   │   ├── empresas.py        # Rotas de empresas
│   │   ├── convenios.py       # Rotas de convênios
│   │   └── dashboard.py       # Rotas do dashboard
│   │
│   ├── services/              # Regras de negócio
│   │   ├── __init__.py
│   │   ├── pdf_service.py     # Geração de PDFs/relatórios
│   │   ├── auth_service.py    # Lógica de autenticação
│   │   ├── vencimento_service.py # Controle de vencimentos
│   │   └── convenio_service.py   # Regras dos convênios
│   │
│   └── utils/                 # Funções auxiliares/utilitárias
│       ├── __init__.py
│       └── helpers.py
│
├── frontend/                  # Interface gráfica em Flet
│   ├── main.py                # Inicialização da interface
│   │
│   ├── views/                 # Telas do sistema
│   │   ├── login.py
│   │   ├── dashboard.py
│   │   ├── empresas.py
│   │   └── convenios.py
│   │
│   └── components/            # Componentes reutilizáveis
│       ├── navbar.py
│       └── cards.py
│
├── database/
│   ├── scripts.sql            # Scripts de criação do banco
│   └── seed.sql               # Dados iniciais/testes
│
├── tests/                     # Testes unitários e integração
│   ├── test_auth.py
│   ├── test_convenios.py
│   ├── test_empresas.py
│   └── test_dashboard.py
│
├── .env                       # Variáveis de ambiente
├── requirements.txt           # Dependências do projeto
├── .gitignore                 # Arquivos ignorados pelo Git
├── README.md                  # Documentação principal
└── run.py                     # Script principal para execução
