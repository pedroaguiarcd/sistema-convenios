from datetime import date, timedelta
from werkzeug.security import generate_password_hash
from backend.database import criar_app_flask, db
from backend.models.empresa import Empresa
from backend.models.usuario import Usuario
from backend.models.convenio import Convenio
 
app = criar_app_flask()
 
with app.app_context():
 
    db.create_all()
    print("[ok] Tables ready.")
 
    # ------------------------------------------------------------------ #
    # Empresas                                                             #
    # ------------------------------------------------------------------ #
 
    empresa1 = Empresa(
        nome="Tech Solutions LTDA",
        cnpj="33.000.167/0001-01",
        email="empresa@teste.com",
        telefone="(86) 4004-0001",
        endereco="Teresina/PI"
    )
 
    empresa2 = Empresa(
        nome="Construtora Norte S/A",
        cnpj="12.345.678/0001-99",
        email="norte@construtora.com",
        telefone="(86) 3232-5555",
        endereco="Parnaíba/PI"
    )
 
    empresa3 = Empresa(
        nome="Saúde & Vida Clínica",
        cnpj="98.765.432/0001-11",
        email="contato@saudvida.com",
        telefone="(86) 9 9999-1234",
        endereco="Picos/PI"
    )
 
    db.session.add_all([empresa1, empresa2, empresa3])
    db.session.flush()  # get IDs before committing
    print(f"[ok] Empresas criadas: {empresa1.nome}, {empresa2.nome}, {empresa3.nome}")
 
    # ------------------------------------------------------------------ #
    # Usuários                                                             #
    # ------------------------------------------------------------------ #
 
    gestor = Usuario(
        nome="Gestor de Convênios",
        email="gestor@teste.com",
        senha=generate_password_hash("123456"),
        perfil="gestor",
        empresa_id=None
    )
 
    empresa_user = Usuario(
        nome="Tech Solutions LTDA",
        email="empresa@teste.com",
        senha=generate_password_hash("empresa123"),
        perfil="empresa",
        empresa_id=empresa1.id
    )
 
    db.session.add_all([gestor, empresa_user])
    print("[ok] Usuários criados: gestor@teste.com / empresa@teste.com")
 
    # ------------------------------------------------------------------ #
    # Convênios                                                            #
    # ------------------------------------------------------------------ #
 
    hoje = date.today()
 
    convenios = [
        # Active, approved, expiring soon (30 days) — shows up as "próximo"
        Convenio(
            empresa_id=empresa1.id,
            nome="Convênio Tech Solutions",
            descricao="Estágio supervisionado em desenvolvimento de software",
            tipo_convenio="supervisionado",
            data_inicio=hoje - timedelta(days=180),
            data_fim=hoje + timedelta(days=25),
            status="ativo",
            telefone="(86) 4004-0001",
            cnpj="33.000.167/0001-01",
            endereco="Teresina/PI",
            responsavel_legal="Marcos Vinicius Almeida",
            aprovado_por="Gestor UESPI",
            data_aprovacao=hoje - timedelta(days=180),
        ),
        # Active, approved, healthy expiry
        Convenio(
            empresa_id=empresa2.id,
            nome="Convênio Construtora Norte",
            descricao="Estágio obrigatório em engenharia civil",
            tipo_convenio="obrigatorio",
            data_inicio=hoje - timedelta(days=60),
            data_fim=hoje + timedelta(days=120),
            status="ativo",
            telefone="(86) 3232-5555",
            cnpj="12.345.678/0001-99",
            endereco="Parnaíba/PI",
            responsavel_legal="Ana Paula Ferreira",
            aprovado_por="Gestor UESPI",
            data_aprovacao=hoje - timedelta(days=60),
        ),
        # Pending approval — shows in gestor's queue
        Convenio(
            empresa_id=empresa3.id,
            nome="Convênio Saúde & Vida",
            descricao="Estágio não obrigatório em enfermagem",
            tipo_convenio="nao_obrigatorio",
            data_inicio=None,
            data_fim=hoje + timedelta(days=365),
            status="pendente",
            telefone="(86) 9 9999-1234",
            cnpj="98.765.432/0001-11",
            endereco="Picos/PI",
            responsavel_legal="Dr. Carlos Mendes",
        ),
        # Expired — shows in histórico
        Convenio(
            empresa_id=empresa1.id,
            nome="Convênio Tech Solutions (anterior)",
            descricao="Estágio supervisionado — ciclo anterior",
            tipo_convenio="supervisionado",
            data_inicio=hoje - timedelta(days=400),
            data_fim=hoje - timedelta(days=10),
            status="ativo",
            telefone="(86) 4004-0001",
            cnpj="33.000.167/0001-01",
            endereco="Teresina/PI",
            responsavel_legal="Marcos Vinicius Almeida",
            aprovado_por="Gestor UESPI",
            data_aprovacao=hoje - timedelta(days=400),
        ),
        # Cancelled — shows in histórico
        Convenio(
            empresa_id=empresa2.id,
            nome="Convênio Cancelado",
            descricao="Parceria de estágio em arquitetura",
            tipo_convenio="obrigatorio",
            data_inicio=hoje - timedelta(days=200),
            data_fim=hoje + timedelta(days=100),
            status="cancelado",
            telefone="(86) 3232-5555",
            cnpj="12.345.678/0001-99",
            endereco="Parnaíba/PI",
            responsavel_legal="Ana Paula Ferreira",
            motivo_cancelamento="Empresa encerrou atividades na região.",
            data_cancelamento=hoje - timedelta(days=30),
        ),
    ]
 
    db.session.add_all(convenios)
    db.session.commit()
    print(f"[ok] {len(convenios)} convênios criados.")
 
    print("\n✅ Seed concluído! Credenciais:")
    print("   Gestor  -> gestor@teste.com  / 123456")
    print("   Empresa -> empresa@teste.com / empresa123")
 
