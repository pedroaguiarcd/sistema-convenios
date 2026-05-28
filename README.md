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
