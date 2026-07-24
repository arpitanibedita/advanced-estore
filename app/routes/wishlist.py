from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.wishlist import Wishlist
from app.models.product import Product

wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/api/wishlist')

@wishlist_bp.route('', methods=['GET'])
@jwt_required()
def get_wishlist():
    user_id = get_jwt_identity()
    wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'items': [item.to_dict() for item in wishlist_items],
        'count': len(wishlist_items)
    }), 200

@wishlist_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400
    
    product = Product.query.get(product_id)
    if not product or not product.is_active:
        return jsonify({'error': 'Product not found'}), 404
    
    existing = Wishlist.query.filter_by(
        user_id=user_id, product_id=product_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Product already in wishlist'}), 409
    
    wishlist_item = Wishlist(
        user_id=user_id,
        product_id=product_id
    )
    
    try:
        db.session.add(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Product added to wishlist',
            'item': wishlist_item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add to wishlist'}), 500

@wishlist_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(product_id):
    user_id = get_jwt_identity()
    wishlist_item = Wishlist.query.filter_by(
        user_id=user_id, product_id=product_id
    ).first()
    
    if not wishlist_item:
        return jsonify({'error': 'Item not in wishlist'}), 404
    
    try:
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({'message': 'Item removed from wishlist'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove from wishlist'}), 500