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
│   ├── models/                # Modelos separados por entidade
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── empresa.py
│   │   ├── convenio.py
│   │   └── dashboard.py
│   │
│   ├── routes/                # Rotas da API
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── empresas.py
│   │   ├── convenios.py
│   │   └── dashboard.py
│   │
│   ├── services/              # Regras de negócio
│   │   ├── __init__.py
│   │   ├── pdf_service.py
│   │   ├── auth_service.py
│   │   ├── vencimento_service.py
│   │   └── convenio_service.py
│   │
│   └── utils/                 # Funções auxiliares
│       ├── __init__.py
│       └── helpers.py
│
├── frontend/                  # Interface Flet
│   ├── main.py
│   │
│   ├── views/                 # Telas
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
│   └── convenios.db           # Banco MySQL
│
├── tests/                     # Testes unitários
│   ├── test_auth.py
│   ├── test_convenios.py
│   ├── test_empresas.py
│   └── test_dashboard.py
│
├── requirements.txt
├── .gitignore
├── README.md
└── run.py                     # Script para rodar a aplicação
