# Zelar Digital

## Como rodar

### 1. Instalar dependências
```bash
python -m pip install -r requirements.txt
```

### 2. Configurar banco
Crie o banco no MySQL:

```sql
CREATE DATABASE zelar_digital;
```

### 3. Configure o .env
```bash
copy .env.example .env
```

### 4. Rodar
```bash
python run.py
```

## Solução de erro MySQLdb OperationalError (2002)

Se aparecer:

Can't connect to server on 'localhost' (10061)

Faça:

1. Ligue o MySQL/MariaDB
2. Troque localhost por 127.0.0.1
3. Verifique porta 3306
4. Ajuste usuário e senha no .env

## Testar conexão

PowerShell:

```powershell
Test-NetConnection 127.0.0.1 -Port 3306
```
