from datetime import timedelta
from ast import literal_eval

from flask_restful import Resource, reqparse, abort
from app.databases_connection import conn_psql as psql
from app.databases_connection import conn_redis as redis

import psycopg2.extras

parser = reqparse.RequestParser()
parser.add_argument('product', type=int)
parser.add_argument('quantity', type=int)


class Cart(Resource):

    def get(self, user_id):
        response = {"total": 0, "quantidade_produtos": 0, "items": []}

        cur = psql.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f"SELECT nome FROM usuarios WHERE id={user_id}")
        user_name = cur.fetchone()
        if user_name is None:
            abort(400)
        response['id_cliente'] = user_id
        response['nome_cliente'] = user_name['nome']

        cart = redis.get(user_id)
        if cart is None:
            cart = b"[]"
        products = literal_eval(cart.decode("utf-8"))

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

    def delete(self, user_id):
        data = parser.parse_args()
        cart = redis.get(user_id)
        if cart is None:
            abort(400)

        produtos = literal_eval(cart.decode("utf-8"))
        remove_index = 0
        for idx in range(len(produtos)):
            produto = produtos[idx]
            if produto.get('produto') == data.get('product'):
                remove_index = idx

        produto = produtos.pop(remove_index)

        redis.setex(
            user_id,
            timedelta(hours=1),
            f'{produtos}')

        return {"msg": "Item removido com sucesso", "produto": produto}
