from app import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    icon = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slug': self.slug,
            'icon': self.icon,
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float)
    stock = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(255))
    images = db.Column(db.JSON)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True, index=True)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='product', lazy=True, cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan')
    wishlist_items = db.relationship('Wishlist', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def get_current_price(self):
        return self.discount_price if self.discount_price else self.price
    
    def get_discount_percentage(self):
        if self.discount_price:
            return round((1 - self.discount_price / self.price) * 100)
        return 0
    
    def to_dict(self, include_images=False):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'category': self.category.to_dict() if self.category else None,
            'price': self.price,
            'discount_price': self.discount_price,
            'current_price': self.get_current_price(),
            'discount_percentage': self.get_discount_percentage(),
            'stock': self.stock,
            'sku': self.sku,
            'image': self.image,
            'rating': self.rating,
            'review_count': self.review_count,
            'is_active': self.is_active,
            'featured': self.featured,
        }
        if include_images:
            data['images'] = self.images
        return data
    
    def __repr__(self):
        return f'<Product {self.name}>'