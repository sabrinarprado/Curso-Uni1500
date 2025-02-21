create database chat_ia_db;
use chat_ia_db;

-- Tabela de usuario
create table usuario(
	idusuario int auto_increment primary key,
    nome varchar(100) not null,
    email varchar(50) unique not null, 
    senha varchar(50) not null
);

-- Tabela de chat
create table chat (
	idchat int auto_increment primary key,
    titulo varchar(100) not null, 
    data_criacao datetime default current_timestamp,
    idusuario int,
    foreign key(idusuario) references usuario(idusuario) on delete cascade
);

-- tabela de mensagens
create table mensagem(
	idmensagem int auto_increment primary key,
    conteudo text not null,
    origem enum('usuario', 'LLM') not null, 
    enviado_em datetime default current_timestamp,
    idusuario int, 
    idchat int, 
    foreign key(idusuario) references usuario(idusuario) on delete cascade,
    foreign key(idchat) references chat(idchat) on delete cascade
);

-- Tabela de fazenda
create table fazenda(
	idfazenda int auto_increment primary key,
    nome varchar(100) not null, 
    municipio varchar(100) not null,
    estado varchar(2) not null
);

-- Tabela de animais inseminados
create table animal_inseminado(
	idanimal_inseminado int auto_increment primary key,
    numero_animal varchar(45) not null,
    lote varchar(45) not null, 
    raca varchar(45) not null, 
    categoria varchar(45) not null, 
    ECC decimal(10,3) not null, 
    ciclicidade tinyint(1) not null,
    idfazenda int,
    foreign key(idfazenda) references fazenda(idfazenda) on delete cascade    
);

-- Tabela de informações sobre a inseminação
create table inseminacao(
	idinseminacao int auto_increment primary key,
    protocolo varchar(45), 
    ECG varchar(45),
    dose_ecg varchar(45), 
    touro varchar(45),
    raca_touro varchar(45),
    empresa_touro varchar(45),
    inseminador varchar(45),
    numero_IATF varchar(45),
    DG tinyint(1),
    vazia tinyint(1),
    com_ou_sem_CL tinyint(1),
    perda tinyint(1),
    idanimal_inseminado int,
    foreign key (idanimal_inseminado) references animal_inseminado(idanimal_inseminado) on delete cascade
);

select * from fazenda;

























