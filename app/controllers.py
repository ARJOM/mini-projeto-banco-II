from datetime import timedelta

from app import api
from flask_restful import Resource, reqparse, abort
from app.databases_connection import conn_psql as psql
from app.databases_connection import conn_redis as redis
import psycopg2.extras
from ast import literal_eval

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('price', type=float)
parser.add_argument('product', type=int)
parser.add_argument('quantity', type=int)


@api.resource("/users")
class User(Resource):
    def get(self):
        cur = psql.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        statement = "SELECT id, nome FROM usuarios"
        cur.execute(statement)
        response = cur.fetchall()
        cur.close()
        return response

    def post(self):
        data = parser.parse_args()
        statement = f"INSERT INTO usuarios(nome) VALUES ('{data.get('name')}')"
        cur = psql.cursor()
        cur.execute(statement)
        psql.commit()
        cur.close()
        return {"msg": "Usuário cadastrado com sucesso"}


@api.resource("/users/<int:id>")
class UserDetail(Resource):
    def get(self, id):
        statement = f"SELECT * FROM usuarios WHERE id={id}"
        cur = psql.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(statement)
        response = cur.fetchone()
        cur.close()
        return response


@api.resource("/products")
class Product(Resource):

    def post(self):
        data = parser.parse_args()
        statement = f"INSERT INTO produtos(descricao, preco) " \
                    f"VALUES ('{data.get('description')}', {data.get('price')})"
        cur = psql.cursor()
        cur.execute(statement)
        psql.commit()
        cur.close()
        return {"msg": "Produto cadastrado com sucesso"}

    def get(self):
        statement = "SELECT * FROM produtos"
        cur = psql.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(statement)
        response = cur.fetchall()
        cur.close()
        return response


@api.resource("/products/<int:id>")
class ProductDetail(Resource):

    def get(self, id):
        statement = f"SELECT * FROM produtos WHERE id={id}"
        cur = psql.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(statement)
        response = cur.fetchone()
        cur.close()
        return response


@api.resource("/carts/<int:user_id>")
class Cart(Resource):
    def get(self, user_id):
        response = {"total": 0, "quantidade_produtos": 0, "items": []}

        cart = redis.get(user_id)
        if cart is None:
            return []
        products = literal_eval(cart.decode("utf-8"))

        cur = psql.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f"SELECT nome FROM usuarios WHERE id={user_id}")
        user_name = cur.fetchone()
        response['cliente'] = user_name['nome']

        for product in products:
            cur.execute(f"SELECT * FROM produtos WHERE id={product['produto']}")
            prod = cur.fetchone()
            prod['quantidade'] = product['quantidade']
            prod['sub-total'] = prod['quantidade'] * prod['preco']
            response['items'].append(prod)

        response['quantidade_produtos'] = len(response['items'])
        response['total'] = sum(x['sub-total'] for x in response['items'])

        return response

    def post(self, user_id):
        # Recebendo dados do corpo da requisição
        data = parser.parse_args()
        item = {'produto': data.get('product'), 'quantidade': data.get('quantity')}

        # Verificando se os dados existem no banco de dados
        cur = psql.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f"SELECT * FROM usuarios WHERE id={user_id}")
        user = cur.fetchone()
        cur.execute(f"SELECT * FROM produtos WHERE id={data.get('product')}")
        product = cur.fetchone()
        cur.close()

        if user is None or product is None:
            abort(400)

        # Recebendo dados do banco para o usuário informado
        cart = redis.get(user_id)
        if cart is None:
            produtos = [item]
        else:
            produtos = literal_eval(cart.decode("utf-8"))

            # Sobreescreve item caso já exista no carrinho
            existia = False
            for idx in range(len(produtos)):
                produto = produtos[idx]
                if produto.get('produto') == item.get('produto'):
                    produto['quantidade'] = item['quantidade']
                    produtos[idx] = produto
                    existia = True

            if not existia:
                produtos.append(item)

        redis.setex(
            user_id,
            timedelta(hours=1),
            f'{produtos}')

        return {"msg": "Item adicionado com sucesso"}
