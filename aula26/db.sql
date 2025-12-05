CREATE database escola;

use escola;

CREATE TABLE professor (
	id_professor int not null auto_increment primary key,
    nome VARCHAR(100) not null,
    rua VARCHAR(300) not null,
    numero int,
    bairro varchar(100),
    cidade varchar(100),
    estado char(2),
    telefone varchar(20)
);
CREATE TABLE aluno (
	id_aluno int not null auto_increment primary key,
    nome VARCHAR(100) not null,
    rua VARCHAR(300) not null,
    numero int,
    bairro varchar(100),
    cidade varchar(100),
    estado char(2),
	telefone varchar(20)
);
CREATE TABLE disciplina (
	id_disciplina int not null auto_increment primary key,
    nome varchar(100),
    horario varchar(50),
    id_professor INT NOT NULL,
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
);
CREATE TABLE aluno_disciplina (
    id_aluno INT NOT NULL,
    id_disciplina INT NOT NULL,
    PRIMARY KEY (id_aluno, id_disciplina),
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno),
    FOREIGN KEY (id_disciplina) REFERENCES disciplina(id_disciplina)
);
CREATE TABLE notas (
    id_nota INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_disciplina INT NOT NULL,
    nota1 DECIMAL(5 , 2 ),
    nota2 DECIMAL(5 , 2 ),
    nota3 DECIMAL(5 , 2 ),
    nota4 DECIMAL(5 , 2 ),
    FOREIGN KEY (id_aluno)
        REFERENCES aluno (id_aluno),
    FOREIGN KEY (id_disciplina)
        REFERENCES disciplina (id_disciplina)
);
CREATE TABLE ee_administracao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO ee_administracao (login, password) 
VALUES 
    ('admin1', MD5('senha123')),
    ('admin2', MD5('senha456')),
    ('admin3', MD5('senha789'));
    
INSERT INTO aluno (nome, rua, numero, bairro, cidade, estado, telefone) VALUES
('Ana Beatriz Silva', 'Rua das Flores', 120, 'Centro', 'São Paulo', 'SP', '(11) 99876-4321'),
('Lucas Almeida Santos', 'Avenida Brasil', 45, 'Jardim Paulista', 'São Paulo', 'SP', '(11) 98765-2109'),
('Mariana Oliveira Costa', 'Rua Rio Branco', 89, 'Boa Vista', 'Campinas', 'SP', '(19) 99123-4455'),
('João Pedro Lima', 'Rua Santa Luzia', 300, 'São José', 'Belo Horizonte', 'MG', '(31) 98234-5566'),
('Rafaela Souza Martins', 'Rua do Sol', 55, 'Centro', 'Curitiba', 'PR', '(41) 99567-8899');

INSERT INTO professor (nome, rua, numero, bairro, cidade, estado, telefone) VALUES
('Carlos Alberto Lima', 'Rua das Palmeiras', 101, 'Centro', 'São Paulo', 'SP', '(11) 99123-4567'),
('Fernanda Souza Oliveira', 'Avenida das Nações', 220, 'Jardim América', 'Campinas', 'SP', '(19) 98877-3344'),
('Rogério Mendes Santos', 'Rua Rio Negro', 56, 'Boa Vista', 'Belo Horizonte', 'MG', '(31) 98211-4455'),
('Patrícia Ribeiro Costa', 'Rua das Rosas', 300, 'Centro', 'Curitiba', 'PR', '(41) 99566-7788'),
('André Luiz Ferreira', 'Avenida Brasil', 789, 'Vila Nova', 'Goiânia', 'GO', '(62) 98433-1122');

INSERT INTO disciplina (nome, horario, id_professor) VALUES
-- Professor 1: Carlos Alberto Lima
('Programação Web com Python', 'Seg 19:00 - 22:00', 1),
('Banco de Dados Relacionais', 'Qua 19:00 - 22:00', 1),
-- Professor 2: Fernanda Souza Oliveira
('Algoritmos e Estrutura de Dados', 'Ter 08:00 - 11:00', 2),
('Introdução à Ciência de Dados', 'Qui 14:00 - 17:00', 2),
-- Professor 3: Rogério Mendes Santos
('Cálculo I', 'Seg 08:00 - 11:00', 3),
('Física Aplicada', 'Sex 10:00 - 13:00', 3),
-- Professor 4: Patrícia Ribeiro Costa
('Língua Portuguesa', 'Ter 19:00 - 21:00', 4),
('Metodologia Científica', 'Qui 19:00 - 21:00', 4),
-- Professor 5: André Luiz Ferreira
('Redes de Computadores', 'Qua 14:00 - 17:00', 5),
('Sistemas Operacionais', 'Sex 19:00 - 22:00', 5);

