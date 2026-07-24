from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.cart import CartItem
from app.models.product import Product

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    total = sum(item.get_total() for item in cart_items)
    
    return jsonify({
        'items': [item.to_dict() for item in cart_items],
        'total': total,
        'count': len(cart_items)
    }), 200

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id or quantity < 1:
        return jsonify({'error': 'Invalid product or quantity'}), 400
    
    product = Product.query.get(product_id)
    if not product or not product.is_active:
        return jsonify({'error': 'Product not found'}), 404
    
    if product.stock < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    cart_item = CartItem.query.filter_by(
        user_id=user_id, product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Product added to cart',
            'item': cart_item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add to cart'}), 500

@cart_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
    
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    data = request.get_json()
    quantity = data.get('quantity')
    
    if not quantity or quantity < 1:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    if cart_item.product.stock < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    cart_item.quantity = quantity
    
    try:
        db.session.commit()
        return jsonify(cart_item.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update cart'}), 500

@cart_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
    
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    try:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item removed from cart'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove item'}), 500