CREATE DATABASE convenios_db;

USE convenios_db;

CREATE TABLE empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cnpj VARCHAR(20),
    email VARCHAR(255),
    telefone VARCHAR(20)
);

CREATE TABLE convenios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT,
    descricao TEXT,
    data_inicio DATE,
    data_fim DATE,
    status VARCHAR(50),

    FOREIGN KEY (empresa_id)
    REFERENCES empresas(id)
);