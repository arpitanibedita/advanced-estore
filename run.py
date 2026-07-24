import os
from app import create_app, db
from app.models.user import User
from app.models.product import Product, Category
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.review import Review
from app.models.wishlist import Wishlist

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Category': Category,
        'Order': Order,
        'OrderItem': OrderItem,
        'CartItem': CartItem,
        'Review': Review,
        'Wishlist': Wishlist
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)