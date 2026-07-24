# Advanced E-Commerce Store

A production-ready, full-stack e-commerce platform built with Python (Flask), PostgreSQL, and responsive HTML/CSS/JavaScript.

## Features

✅ **User Authentication**
- JWT token-based authentication
- User registration, login, password reset
- User profiles and order history

✅ **Product Management**
- Product catalog with categories and filtering
- Advanced search functionality
- Product details, images, and pricing
- Inventory management

✅ **Shopping Experience**
- Shopping cart
- Wishlist functionality
- Product reviews and ratings
- Sort and filter options

✅ **Order Management**
- Checkout process
- Order tracking and history
- Order status notifications
- Invoice generation

✅ **Payment Integration**
- Stripe payment gateway integration
- Multiple payment methods
- Order confirmation emails

✅ **Admin Dashboard**
- Manage products (CRUD operations)
- Manage categories
- View orders and sales
- Inventory management
- Sales analytics and reports

✅ **Responsive Design**
- Mobile-first approach
- Cross-browser compatibility
- Modern UI/UX

## Tech Stack

### Backend
- **Python 3.9+**
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin requests
- **Stripe** - Payment processing
- **python-dotenv** - Environment variables

### Database
- **PostgreSQL** - Primary database

### Frontend
- **HTML5**
- **CSS3** (with responsive design)
- **JavaScript (Vanilla + Fetch API)**
- **Bootstrap 5** - CSS framework

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/arpitanibedita/advanced-estore.git
cd advanced-estore
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Setup database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the application
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get product details
- `GET /api/products/categories` - Get all categories
- `GET /api/products/<id>/reviews` - Get product reviews

### Cart
- `GET /api/cart` - Get cart items
- `POST /api/cart/add` - Add to cart
- `PUT /api/cart/<item_id>` - Update cart item
- `DELETE /api/cart/<item_id>` - Remove from cart

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders` - Get user orders
- `GET /api/orders/<id>` - Get order details

### Reviews
- `POST /api/reviews` - Add review
- `DELETE /api/reviews/<id>` - Delete review

### Wishlist
- `GET /api/wishlist` - Get wishlist
- `POST /api/wishlist/add` - Add to wishlist
- `DELETE /api/wishlist/<product_id>` - Remove from wishlist

### Admin
- `POST /api/admin/products` - Create product
- `PUT /api/admin/products/<id>` - Update product
- `DELETE /api/admin/products/<id>` - Delete product
- `GET /api/admin/orders` - Get all orders
- `GET /api/admin/analytics` - Get sales analytics

## Project Structure

```
advanced-estore/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── cart.py
│   │   ├── review.py
│   │   └── wishlist.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   ├── orders.py
│   │   ├── reviews.py
│   │   ├── wishlist.py
│   │   ├── admin.py
│   │   └── users.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── decorators.py
│   │   └── email_service.py
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── main.js
│           ├── cart.js
│           └── admin.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── product_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── user/
│   │   ├── dashboard.html
│   │   └── profile.html
│   └── admin/
│       ├── dashboard.html
│       └── products.html
├── migrations/
├── tests/
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Usage

1. **Browse Products** - Navigate to the homepage to see all products
2. **Search & Filter** - Use search and filter options to find products
3. **Add to Cart** - Click "Add to Cart" button on product pages
4. **Checkout** - Proceed to checkout and enter payment details
5. **Track Orders** - View order history in user dashboard
6. **Admin Panel** - Access admin dashboard to manage products and orders

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License

## Support

For support, email support@estore.com or open an issue on GitHub.