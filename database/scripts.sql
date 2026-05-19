CREATE DATABASE convenios_db;

USE convenios_db;

CREATE TABLE empresas (
    id INT PRIMARY KEY, AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cnpj VARCHAR(20),
    email VARCHAR(255),
    telefone VARCHAR(20)
);

CREATE TABLE convenios (
    id INT PRIMARY KEY, AUTO_INCREMENT,
    empresa_id INT,
    descricao TEXT,
    data_inicio DATE,
    data_fim DATE,
    status VARCHAR(50),

    FOREIGN KEY (empresa_id)
    REFERENCES empresas(id)
);

-- CREATE TABLE `convenios` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `empresa_id` int(11) NOT NULL,
--   `descricao` text NOT NULL,
--   `data_inicio` date NOT NULL,
--   `data_fim` date NOT NULL,
--   `status` enum('ativo','pendente','vencido','cancelado') DEFAULT 'pendente',
--   `observacoes` text DEFAULT NULL,
--   `created_at` timestamp NULL DEFAULT current_timestamp(),
--   PRIMARY KEY (`id`),
--   KEY `empresa_id` (`empresa_id`),
--   CONSTRAINT `1` FOREIGN KEY (`empresa_id`) REFERENCES `empresas` (`id`) ON DELETE CASCADE
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |

-- CREATE TABLE `empresas` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `nome` varchar(255) NOT NULL,
--   `cnpj` varchar(20) DEFAULT NULL,
--   `email` varchar(255) DEFAULT NULL,
--   `telefone` varchar(20) DEFAULT NULL,
--   `endereco` text DEFAULT NULL,
--   `created_at` timestamp NULL DEFAULT current_timestamp(),
--   PRIMARY KEY (`id`),
--   UNIQUE KEY `cnpj` (`cnpj`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |

-- CREATE TABLE `usuarios` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `nome` varchar(100) NOT NULL,
--   `email` varchar(100) NOT NULL,
--   `senha` varchar(100) DEFAULT NULL,
--   `created_at` timestamp NULL DEFAULT current_timestamp(),
--   PRIMARY KEY (`id`),
--   UNIQUE KEY `email` (`email`),
--   UNIQUE KEY `senha` (`senha`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |