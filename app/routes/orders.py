from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.product import Product
from datetime import datetime
import stripe
import os

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_user_orders():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    orders = Order.query.filter_by(user_id=user_id).order_by(
        Order.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'orders': [order.to_dict(include_items=True) for order in orders.items],
        'total': orders.total,
        'pages': orders.pages,
        'current_page': page
    }), 200

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(order.to_dict(include_items=True)), 200

@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    shipping_address = data.get('shipping_address')
    if not shipping_address:
        return jsonify({'error': 'Shipping address required'}), 400
    
    order = Order(
        user_id=user_id,
        shipping_address=shipping_address,
        billing_address=data.get('billing_address', shipping_address),
        payment_method=data.get('payment_method', 'credit_card'),
        status='pending'
    )
    
    for cart_item in cart_items:
        order_item = OrderItem(
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.get_current_price()
        )
        order.order_items.append(order_item)
        cart_item.product.stock -= cart_item.quantity
    
    order.calculate_total()
    order.tax = order.subtotal * 0.1
    order.shipping_cost = 10.0 if order.subtotal < 100 else 0.0
    order.total = order.subtotal + order.tax + order.shipping_cost
    
    try:
        db.session.add(order)
        for cart_item in cart_items:
            db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict(include_items=True)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create order'}), 500