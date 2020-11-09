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
    MONGO_DB_NAME=
    MONGO_HOST=
    MONGO_PORT=
    ``` 
6. Executar o servidor do projeto
    ```
    python run.py
    ```

## Requisições

### Usuários

 URL | Método | Descrição 
------|------------|-----
/users | POST | Recurso de criação de usuário, espera um json no corpo da requisição
/users | GET | Recurso de listagem de usuário, lista todos os usuários registrados
/users/:id | GET | Recurso de detalhe de usuário, espera o id do usuário na url

Para registrar um usuário usando a rota `/users`, o corpo da requisição deve ser assim:
```
{
    "name": "Antônio Ricart"
}
```

 

### Produtos

 URL | Método | Descrição 
------|------------|-----
/products | POST | Recurso de criação de produto, espera um json no corpo da requisição
/products | GET | Recurso de listagem de produto, lista todos os usuários registrados
/products/:id | GET | Recurso de detalhe de produto, espera o id do produto na url

Para registrar um produto usando a rota `/products`, o corpo da requisição deve ser assim:
```
{
	"description": "Guarda-chuva",
	"price": 26.78
}
```

### Carrinho

 URL | Método | Descrição 
------|------------|-----
/cart/:id | POST | Recurso de adição de produto ao carrinho, espera um json no corpo da requisição com os dados do produto, e o id do usuário na url 
/cart/:id | GET | Recurso de listagem do carrinho de um usuário, espera o id do usuário na url
/cart/:id | DELETE | Recurso de remoção de produto do carrinho, espera o id do usuário na url e o id do produto no corpo da requisição

Para adicionar um item ao carrinho de um usuário na rota `/cart/:id`, o corpo da requisição deve ser assim:
```
{
    "product": 1,
    "quantity": 1
}
```
Para remover um item do carrinho de um usuário na rota `/cart/:id`, o corpo da requisição deve ser assim:
```
{
    "product": 1,
}
```

Caso já exista um produto no carrinho com o id informado, o valor da quantidade é sobreescrito

### Pedidos
URL | Método | Descrição 
------|------------|-----
/orders/:id | POST | Recurso de criação de pedido, espera o id do usuário na url
/orders | GET |  Recurso de listaem de todos pedidos
/orders/:id | GET | Recurso de lisgagem de pedidos de um usuário específico, espera o id do usuário na url
/orders/products/:id | GET | Recurso de listagem de pedidos que contenha um produto específico, espera o id do produto na url
