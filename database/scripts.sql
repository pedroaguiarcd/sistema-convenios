CREATE DATABASE IF NOT EXISTS convenios_db;

USE convenios_db;

DROP TABLE IF EXISTS convenios;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS empresas;

CREATE TABLE empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cnpj VARCHAR(30),
    email VARCHAR(255),
    telefone VARCHAR(20),
    endereco VARCHAR(255)
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    perfil ENUM(
        'empresa',
        'gestor',
        'admin'
    ) NOT NULL,
    empresa_id INT NULL,

    FOREIGN KEY (empresa_id)
    REFERENCES empresas(id)
);

CREATE TABLE convenios (
    id INT AUTO_INCREMENT PRIMARY KEY,

    empresa_id INT NOT NULL,

    descricao VARCHAR(100) NOT NULL,

    tipo_convenio ENUM(
        'obrigatorio',
        'nao_obrigatorio',
        'supervisionado'
    ) NOT NULL DEFAULT 'supervisionado',

    data_inicio DATE NULL,

    data_fim DATE NOT NULL,

    status ENUM(
        'ativo',
        'pendente',
        'cancelado'
    ) NOT NULL DEFAULT 'pendente',

    telefone VARCHAR(20),

    cnpj VARCHAR(100) NOT NULL,

    endereco VARCHAR(255),

    responsavel_legal VARCHAR(100),

    data_aprovacao DATE,

    data_cancelamento DATE,

    aprovado_por VARCHAR(100),

    motivo_cancelamento VARCHAR(255),

    alterado_em DATETIME,

    excluido_em DATETIME,

    motivo_alteracao VARCHAR(255),

    campos_alterados TEXT,

    motivo_exclusao VARCHAR(255),

    deletado BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (empresa_id)
    REFERENCES empresas(id)
);