from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product, Category

products_bp = Blueprint('products', __name__, url_prefix='/api/products')

@products_bp.route('', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    category_id = request.args.get('category_id', None, type=int)
    search = request.args.get('search', '', type=str)
    sort = request.args.get('sort', 'latest', type=str)
    
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(
            (Product.name.ilike(f'%{search}%')) |
            (Product.description.ilike(f'%{search}%'))
        )
    
    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort == 'rating':
        query = query.order_by(Product.rating.desc())
    elif sort == 'featured':
        query = query.filter_by(featured=True)
    else:
        query = query.order_by(Product.created_at.desc())
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'products': [product.to_dict() for product in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    }), 200

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    
    if not product or not product.is_active:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify(product.to_dict(include_images=True)), 200

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify({
        'categories': [category.to_dict() for category in categories]
    }), 200

@products_bp.route('/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    from app.models.review import Review
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    reviews = Review.query.filter_by(product_id=product_id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'reviews': [review.to_dict() for review in reviews.items],
        'total': reviews.total,
        'pages': reviews.pages,
        'average_rating': product.rating
    }), 200