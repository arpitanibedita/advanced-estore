from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User, Address

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.phone = data.get('phone', user.phone)
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500

@users_bp.route('/addresses', methods=['GET'])
@jwt_required()
def get_addresses():
    user_id = get_jwt_identity()
    addresses = Address.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'addresses': [addr.to_dict() for addr in addresses]
    }), 200

@users_bp.route('/addresses', methods=['POST'])
@jwt_required()
def add_address():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    address = Address(
        user_id=user_id,
        address_type=data.get('address_type', 'shipping'),
        street=data.get('street'),
        city=data.get('city'),
        state=data.get('state'),
        postal_code=data.get('postal_code'),
        country=data.get('country'),
        is_default=data.get('is_default', False)
    )
    
    try:
        db.session.add(address)
        db.session.commit()
        
        return jsonify({
            'message': 'Address added successfully',
            'address': address.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add address'}), 500