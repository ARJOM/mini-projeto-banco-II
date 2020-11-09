from datetime import date, datetime
from flask import request
from flask_restful import Resource, abort
from app.controllers.cart_controllers import Cart
from app.databases_connection import conn_mongo as mongo
from app.databases_connection import conn_redis as redis


class Order(Resource):

    def get(self):
        colecao = mongo.orders
        result = []
        for order in colecao.find():
            order['_id'] = str(order['_id'])
            result.append(order)
        return result


class OrderList(Resource):

    def post(self, user_id):
        colecao = mongo.orders
        cart = Cart()
        obj = cart.get(user_id)
        if len(obj['items']) == 0:
            abort(400)
        obj['hora'] = datetime.now().strftime('%H:%M')
        obj['data'] = date.today().strftime('%d/%m/%Y')
        redis.set(user_id, "[]")
        colecao.insert_one(obj)
        return 200

    def get(self, user_id):
        colecao = mongo.orders
        result = []
        for order in colecao.find({'id_cliente': user_id}):
            order['_id'] = str(order['_id'])
            result.append(order)
        return result


class ProductOrderList(Resource):

    def get(self, product_id):
        colecao = mongo.orders
        result = []
        for order in colecao.find():
            order['_id'] = str(order['_id'])
            for product in order['items']:
                if product['id'] == product_id:
                    result.append(order)
                    break
        return result
