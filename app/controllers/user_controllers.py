from flask_restful import Resource, reqparse
from app.databases_connection import conn_psql as psql
import psycopg2.extras

parser = reqparse.RequestParser()
parser.add_argument('name')


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


class UserDetail(Resource):

    def get(self, user_id):
        statement = f"SELECT * FROM usuarios WHERE id={user_id}"
        cur = psql.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(statement)
        response = cur.fetchone()
        cur.close()
        return response
