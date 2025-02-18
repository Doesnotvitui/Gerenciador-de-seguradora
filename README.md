# Gerenciador de Seguradora

Este projeto é um sistema de gerenciamento de seguradora desenvolvido em Python, utilizando a biblioteca PyQt5 para a interface gráfica e SQLAlchemy para a interação com o banco de dados MySQL. O sistema permite a manipulação de dados relacionados a clientes, apartamentos, apólices e acidentes, oferecendo funcionalidades como adição, exclusão e consulta de registros.

## Funcionalidades

- **Login de Usuário**: O sistema exige autenticação para acessar as funcionalidades principais.
- **Gerenciamento de Clientes**: Permite adicionar, visualizar e excluir clientes.
- **Gerenciamento de Apartamentos**: Permite adicionar, visualizar e excluir apartamentos associados a clientes.
- **Gerenciamento de Apólices**: Permite adicionar, visualizar e excluir apólices associadas a clientes e apartamentos.
- **Gerenciamento de Acidentes**: Permite adicionar, visualizar e excluir registros de acidentes associados a clientes, apartamentos e apólices.
- **Consulta Avançada**: Permite a execução de consultas SQL personalizadas diretamente na interface.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **PyQt5**: Biblioteca para criação da interface gráfica.
- **SQLAlchemy**: ORM (Object-Relational Mapping) para interação com o banco de dados.
- **MySQL**: Banco de dados relacional utilizado para armazenar os dados.

## Estrutura do Banco de Dados

O banco de dados é composto pelas seguintes tabelas:

- **Cliente**: Armazena informações dos clientes, como nome, CPF, RG e e-mail.
- **Apartamento**: Armazena informações dos apartamentos, como número, bloco, valor e o cliente associado.
- **Apolice**: Armazena informações das apólices, como valor assegurado, cliente e apartamento associados.
- **Acidentes**: Armazena informações sobre acidentes, incluindo quantidade, cliente, apartamento e apólice associados.
