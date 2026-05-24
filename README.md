# Zelar Digital

# Integrantes do Grupo
Enzo Lacerda
João Victor Silva
Lucas Gomes
Rízia Araujo
Thiago Amorim

## Descrição do Sistema

O Zelar Digital é uma plataforma web desenvolvida para facilitar a comunicação entre cidadãos e órgãos responsáveis pela manutenção urbana. O sistema permite que usuários registrem ocorrências urbanas, como buracos, problemas de iluminação pública, descarte irregular de lixo e outras demandas da cidade.

As ocorrências podem incluir descrição, imagem e localização geográfica, sendo exibidas em um mapa interativo para melhor visualização e acompanhamento.

---

## Tecnologias Utilizadas

### Backend
- Python
- Flask
- Flask-Login
- Flask-MySQLdb

### Frontend
- HTML5
- CSS3
- JavaScript

### Banco de Dados
- MySQL

### Bibliotecas e APIs
- Leaflet.js
- OpenStreetMap
- Werkzeug
- Python Dotenv

### Controle de Versão
- Git
- GitHub

---

## Funcionalidades Implementadas

- Cadastro de usuários
- Login e autenticação
- Logout de usuários
- Registro de ocorrências urbanas
- Upload de imagens
- Geolocalização automática
- Exibição de ocorrências em mapa interativo
- Listagem de ocorrências
- Integração com banco de dados MySQL

---

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/rizia-araujo/zelar-digital.git

### 2.  Entrar na pasta do projeto
cd zelar-digital

### 3. Criar ambiente virtual
python -m venv venv

### 4. Ativar ambiente virtual
Windows CMD
venv\Scripts\activate
Windows PowerShell
.\venv\Scripts\Activate.ps1

### 5. Instalar dependências
python -m pip install -r requirements.txt

### 6. Criar banco de dados

No MySQL:

CREATE DATABASE zelar_digital;

### 7. Configurar variáveis de ambiente

Copie o arquivo:

copy .env.example .env

Configure os dados do MySQL no arquivo .env.

Exemplo:

MYSQL_HOST=127.0.0.1
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha
MYSQL_DB=zelar_digital

SECRET_KEY=123456

### 8. Executar o projeto
python run.py

### Solução de Erro MySQLdb OperationalError (2002)

Se aparecer o erro:

Can't connect to server on 'localhost' (10061)

Verifique:

Se o MySQL/MariaDB está ligado
Se a porta 3306 está ativa
Se usuário e senha estão corretos no .env
Troque localhost por 127.0.0.1

Teste a conexão:

Test-NetConnection 127.0.0.1 -Port 3306
