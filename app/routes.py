from app import api
from app.controllers.user_controllers import User, UserDetail
from app.controllers.product_controllers import Product, ProductDetail
from app.controllers.cart_controllers import Cart
from app.controllers.order_controller import Order, NewOrder

# Rotas de usuários
api.add_resource(UserDetail, '/users/<int:user_id>')
api.add_resource(User, '/users')

# Rotas de produtos
api.add_resource(Product, '/products')
api.add_resource(ProductDetail, '/products/<int:product_id>')

# Rotas do carrinho
api.add_resource(Cart, '/carts/<int:user_id>')

# Rotas de pedido
api.add_resource(Order, '/orders')
api.add_resource(NewOrder, '/orders/<int:user_id>')
