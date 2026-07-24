from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.review import Review
from app.models.product import Product
from app.models.order import Order, OrderItem

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')

@reviews_bp.route('', methods=['POST'])
@jwt_required()
def create_review():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    product_id = data.get('product_id')
    rating = data.get('rating')
    title = data.get('title', '').strip()
    comment = data.get('comment', '').strip()
    
    if not all([product_id, rating, title]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not (1 <= rating <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    order_item = db.session.query(OrderItem).join(Order).filter(
        Order.user_id == user_id,
        OrderItem.product_id == product_id,
        Order.payment_status == 'completed'
    ).first()
    
    existing_review = Review.query.filter_by(
        user_id=user_id, product_id=product_id
    ).first()
    
    if existing_review:
        return jsonify({'error': 'You have already reviewed this product'}), 409
    
    review = Review(
        user_id=user_id,
        product_id=product_id,
        rating=rating,
        title=title,
        comment=comment,
        is_verified=order_item is not None
    )
    
    try:
        db.session.add(review)
        
        all_reviews = Review.query.filter_by(product_id=product_id).all()
        avg_rating = sum(r.rating for r in all_reviews) / (len(all_reviews) + 1)
        product.rating = round(avg_rating, 1)
        product.review_count = len(all_reviews) + 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review created successfully',
            'review': review.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create review'}), 500

@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    user_id = get_jwt_identity()
    review = Review.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    if review.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        product = review.product
        db.session.delete(review)
        
        remaining_reviews = Review.query.filter_by(product_id=product.id).all()
        if remaining_reviews:
            avg_rating = sum(r.rating for r in remaining_reviews) / len(remaining_reviews)
            product.rating = round(avg_rating, 1)
        else:
            product.rating = 0.0
        product.review_count = len(remaining_reviews)
        
        db.session.commit()
        
        return jsonify({'message': 'Review deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete review'}), 500