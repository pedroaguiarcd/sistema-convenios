# ConvênioMgr — Sistema de Gestão Inteligente de Convênios

> MVP técnico e funcional do módulo de monitoramento automatizado e dashboard gerencial de convênios institucionais de estágio.

---

## Stack

| Camada     | Tecnologia                  |
|------------|-----------------------------|
| Backend    | Python 3.11+ · Flask 3.x    |
| Frontend   | Python · Flet 0.23          |
| Banco      | SQLite (via SQLAlchemy)      |
| Scheduler  | APScheduler (background)    |
| Versionamento | Git / GitHub             |

---

## Estrutura do Projeto

```
project/
├── backend/
│   ├── app/
│   │   ├── config/         # Configurações desacopladas
│   │   ├── models/         # SQLAlchemy models
│   │   ├── repositories/   # Repository Pattern
│   │   ├── services/       # Regras de negócio
│   │   ├── routes/         # Blueprints Flask (REST API)
│   │   ├── scheduler/      # Agente de monitoramento automático
│   │   └── utils/          # Logging, error handlers
│   ├── database/           # Arquivo .db SQLite
│   ├── tests/
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── pages/              # Dashboard, Convênios, Monitoramento
│   ├── components/         # Sidebar, MetricCard, CriticalTable
│   ├── services/           # API client HTTP
│   ├── styles/             # Tema, cores, helpers visuais
│   └── main.py
│
├── docs/
├── .env.example
├── .gitignore
└── README.md
```

---

## Instalação e Execução

### Pré-requisitos
- Python 3.11+
- pip

### 1. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite .env conforme necessário
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
python run.py
```

O backend sobe em `http://localhost:5000`.

### 3. Frontend

```bash
cd frontend
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

---

## API REST — Endpoints

### Convênios
| Método | Rota               | Descrição             |
|--------|--------------------|------------------------|
| GET    | /convenios         | Listar (com filtros)   |
| GET    | /convenios/<id>    | Buscar por ID          |
| POST   | /convenios         | Criar novo             |
| PUT    | /convenios/<id>    | Atualizar              |
| DELETE | /convenios/<id>    | Soft delete            |

### Dashboard
| Método | Rota                  | Descrição                    |
|--------|-----------------------|-------------------------------|
| GET    | /dashboard/metrics    | Cards gerenciais              |
| GET    | /dashboard/critical   | Painel de criticidade         |

### Monitoramento
| Método | Rota                      | Descrição                    |
|--------|---------------------------|-------------------------------|
| POST   | /monitoramento/run        | Executar agente manualmente   |
| GET    | /monitoramento/logs       | Histórico de execuções        |
| GET    | /monitoramento/logs/ultimo| Último log                    |

### Saúde
| Método | Rota     | Descrição    |
|--------|----------|--------------|
| GET    | /health  | Health check |

**Filtros disponíveis em GET /convenios:**
- `?status=Vigente`
- `?empresa=NomeDaEmpresa`
- `?tipo=Estágio`

---

## Regras de Negócio — Monitoramento

| Condição              | Status                   |
|-----------------------|--------------------------|
| Expirado (delta < 0)  | 🔴 Vencido               |
| ≤ 30 dias (delta ≤ 30)| 🟡 Próximo do vencimento  |
| > 30 dias             | 🟢 Vigente               |

O agente executa automaticamente a cada 24h via APScheduler e também na inicialização do servidor.

---

## Arquitetura e Padrões

- **Repository Pattern** — separação total entre persistência e lógica
- **Service Layer** — regras de negócio isoladas dos controllers
- **Clean Code** — nomenclatura consistente, funções pequenas, responsabilidade única
- **Soft Delete** — campo `ativo` para exclusão lógica
- **Logs rotativos** — `backend/logs/app.log` (5MB, 3 backups)
- **Tratamento global de erros** — handlers 404, 422, 500
- **CORS configurável** via `.env`

---

## Preparado Para

- [ ] Migração para PostgreSQL (trocar `DATABASE_URL` no `.env`)
- [ ] Autenticação JWT
- [ ] Notificações por e-mail (SMTP)
- [ ] Deploy em container Docker
- [ ] Multi-tenant
- [ ] Integração com cron job externo (`POST /monitoramento/run`)

---

## Dados de Exemplo

Na primeira execução, o banco é populado automaticamente com 8 convênios de exemplo cobrindo todos os status (vigentes, próximos e vencidos), facilitando a visualização imediata do dashboard.

---

## Licença

Projeto acadêmico / institucional — MVP.
