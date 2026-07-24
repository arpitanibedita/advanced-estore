from app import db
from datetime import datetime
import uuid

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True, default=lambda: str(uuid.uuid4())[:8])
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')
    subtotal = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, default=0.0)
    shipping_cost = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, nullable=False)
    
    # Shipping & Billing
    shipping_address = db.Column(db.JSON, nullable=False)
    billing_address = db.Column(db.JSON)
    
    # Payment
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50), default='pending')
    stripe_payment_id = db.Column(db.String(255))
    
    # Additional info
    notes = db.Column(db.Text)
    tracking_number = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    shipped_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def calculate_total(self):
        self.subtotal = sum(item.price * item.quantity for item in self.order_items)
        self.total = self.subtotal + self.tax + self.shipping_cost
        return self.total
    
    def to_dict(self, include_items=False):
        data = {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'status': self.status,
            'payment_status': self.payment_status,
            'subtotal': self.subtotal,
            'tax': self.tax,
            'shipping_cost': self.shipping_cost,
            'total': self.total,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tracking_number': self.tracking_number,
        }
        if include_items:
            data['items'] = [item.to_dict() for item in self.order_items]
        return data
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'product_image': self.product.image if self.product else None,
            'quantity': self.quantity,
            'price': self.price,
            'total': self.quantity * self.price,
        }