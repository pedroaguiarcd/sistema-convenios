USE convenios_db;

INSERT INTO empresas (
    nome,
    cnpj,
    email,
    telefone,
    endereco
)
VALUES (
    'Tech Solutions LTDA',
    '33.000.167/0001-01',
    'empresa@teste.com',
    '(92) 4004-0001',
    'Manaus/AM'
);

INSERT INTO usuarios (
    nome,
    email,
    senha,
    perfil,
    empresa_id
)
VALUES (
    'Gestor de Convênios',
    'gestor@teste.com',
    '123456',
    'gestor',
    NULL
);

INSERT INTO usuarios (
    nome,
    email,
    senha,
    perfil,
    empresa_id
)
VALUES (
    'Tech Solutions LTDA',
    'empresa@teste.com',
    '123456',
    'empresa',
    1
);

INSERT INTO convenios (
    empresa_id,
    descricao,
    tipo_convenio,
    data_inicio,
    data_fim,
    status,
    telefone,
    cnpj,
    endereco,
    responsavel_legal,
    documento_anexo,
    arquivo_documento,
    data_aprovacao,
    aprovado_por
)
VALUES (
    1,
    'Convênio de estágio supervisionado em desenvolvimento de software',
    'supervisionado',
    '2026-01-10',
    '2026-06-30',
    'ativo',
    '(92) 4004-0001',
    '33.000.167/0001-01',
    'Manaus/AM',
    'Marcos Vinicius Almeida',
    NULL,
    NULL,
    '2026-01-10',
    'Gestor UESPI'
);