from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.product import Product, Category
from app.models.order import Order
from datetime import datetime, date

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def check_admin(func):
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin_bp.route('/products', methods=['POST'])
@jwt_required()
@check_admin
def create_product():
    data = request.get_json()
    
    product = Product(
        name=data.get('name'),
        slug=data.get('slug'),
        description=data.get('description'),
        category_id=data.get('category_id'),
        price=data.get('price'),
        discount_price=data.get('discount_price'),
        stock=data.get('stock', 0),
        sku=data.get('sku'),
        image=data.get('image'),
        images=data.get('images')
    )
    
    try:
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create product'}), 500

@admin_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
@check_admin
def update_product(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.discount_price = data.get('discount_price', product.discount_price)
    product.stock = data.get('stock', product.stock)
    product.image = data.get('image', product.image)
    product.is_active = data.get('is_active', product.is_active)
    product.featured = data.get('featured', product.featured)
    
    try:
        db.session.commit()
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update product'}), 500

@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
@check_admin
def delete_product(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    try:
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete product'}), 500

@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
@check_admin
def get_all_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', None, type=str)
    
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'orders': [order.to_dict(include_items=True) for order in orders.items],
        'total': orders.total,
        'pages': orders.pages,
        'current_page': page
    }), 200

@admin_bp.route('/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
@check_admin
def update_order(order_id):
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    data = request.get_json()
    
    order.status = data.get('status', order.status)
    order.payment_status = data.get('payment_status', order.payment_status)
    order.tracking_number = data.get('tracking_number', order.tracking_number)
    
    try:
        db.session.commit()
        
        return jsonify({
            'message': 'Order updated successfully',
            'order': order.to_dict(include_items=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update order'}), 500

@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
@check_admin
def get_analytics():
    today = datetime.utcnow().date()
    today_orders = Order.query.filter(
        Order.created_at >= datetime.combine(today, datetime.min.time())
    ).all()
    today_sales = sum(o.total for o in today_orders if o.payment_status == 'completed')
    
    first_day = date.today().replace(day=1)
    month_orders = Order.query.filter(Order.created_at >= first_day).all()
    month_sales = sum(o.total for o in month_orders if o.payment_status == 'completed')
    
    total_products = Product.query.count()
    total_users = User.query.count()
    
    return jsonify({
        'today_sales': today_sales,
        'month_sales': month_sales,
        'total_products': total_products,
        'total_users': total_users,
        'total_orders': Order.query.count()
    }), 200