## Executando
1. Criar ambiente virtual
    ```
    python3 -m venv venv
    ```
2. Ativar ambiente virtual
    ```
    source venv/bin/activate
    ```
   2.1. Atualizar o pip
   ```
    pip install --upgrade pip
    ```
3. Instalar dependências
    ```
    pip install -r requirements.txt
    ```
4. Configurar banco de dados postgres e redis, e criar as seguintes tabelas no postgres
    ```sql
    CREATE TABLE produtos(
        id SERIAL,
        descricao TEXT,
        preco FLOAT,
        CONSTRAINT pk_product PRIMARY KEY (id)
    );
    
    CREATE TABLE usuarios(
        id SERIAL,
        nome VARCHAR(255),
        CONSTRAINT pk_user PRIMARY KEY (id)
    )
    ```

5. Criar arquivo .env na raiz do projeto, e preencher o seguinte modelo
    ```
    REDIS_HOST=
    REDIS_PORT=
    PSQL_HOST=
    PSQL_USER=
    PSQL_PASSWORD=
    DB_NAME=
    ``` 
6. Executar o servidor do projeto
    ```
    python run.py
    ```
