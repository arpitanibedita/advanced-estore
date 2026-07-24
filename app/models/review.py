from app import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=False)
    helpful_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'product_id': self.product_id,
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'is_verified': self.is_verified,
            'helpful_count': self.helpful_count,
            'created_at': self.created_at.isoformat(),
        }
    
    def __repr__(self):
        return f'<Review product:{self.product_id} rating:{self.rating}>'