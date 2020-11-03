from flask_restful import Resource, reqparse
from app.databases_connection import conn_psql as psql
import psycopg2.extras

parser = reqparse.RequestParser()
parser.add_argument('description')
parser.add_argument('price', type=float)
parser.add_argument('product', type=int)
parser.add_argument('quantity', type=int)


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


class ProductDetail(Resource):

    def get(self, product_id):
        statement = f"SELECT * FROM produtos WHERE id={product_id}"
        cur = psql.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(statement)
        response = cur.fetchone()
        cur.close()
        return response
