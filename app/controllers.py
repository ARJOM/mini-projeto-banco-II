from app import api
from flask_restful import Resource, reqparse
from app.databases_connection import conn_psql as psql
from app.databases_connection import conn_redis as redis
import psycopg2.extras

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('price', type=float)


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
