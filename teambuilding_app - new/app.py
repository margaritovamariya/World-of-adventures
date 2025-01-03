from flask import Flask, jsonify, render_template, make_response, request, g
from extensions import db, bcrypt  # Импортираме db и bcrypt от extensions.py
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity, get_jwt, unset_jwt_cookies, jwt_required
import stripe
from dotenv import load_dotenv
import os
from flask_migrate import Migrate  # Импортираме Migrate
import uuid


# Зареждаме ключовете от .env файл
load_dotenv()

app = Flask(__name__)

# Stripe API ключ
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_51QZZO3H1yX50wwJ4GcdEXlQ3gUccApMN9VtOMuHhtphQCYdj20BIHylhbUxNk3vumNZK9buw0nwz2nS3GtRjEE6a00EaS0aRlR')

# Настройки за секретен ключ и JWT
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'my_super_secret_key_12345')  # Заредено от .env или по подразбиране
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'my_jwt_secret_key')  # Заредено от .env или по подразбиране
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Активиране на cookies за токени
app.config['JWT_COOKIE_SECURE'] = False  # За тестови цели (True за продукция с HTTPS)
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'  # Име на cookie за JWT
app.config['JWT_COOKIE_CSRF_PROTECT'] = False


# Настройки за базата данни
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация на разширения
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Добавяме миграция
migrate = Migrate(app, db)  # Тук се инициализира Flask-Migrate

# Регистрация на маршрути
from routes.auth import auth
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.payment_routes import payment_bp
from routes.department_routes import department_bp
from routes.category_routes import category_bp
from routes.product_routes import product_bp
from routes.orders_routes import order_bp


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(cart_bp, url_prefix='/api')
app.register_blueprint(payment_bp, url_prefix='/api')
app.register_blueprint(department_bp, url_prefix='/api')
app.register_blueprint(category_bp, url_prefix='/api')
app.register_blueprint(order_bp, url_prefix='/orders')


from models import CartItem, Product, User, Order, OrderItem

@app.before_request
def set_tracking_and_user_id():
    
    """
    Set tracking_id and user_id in the g object for each request.
    """
    # Initialize default values
    g.tracking_id = None
    g.user_id = None
    g.set_tracking_id_cookie = False

    # Get or generate tracking_id
    tracking_id = request.cookies.get('trackingId', None)
    if not tracking_id:
        tracking_id = str(uuid.uuid4())
        g.tracking_id = tracking_id
        g.set_tracking_id_cookie = True
    else:
        g.tracking_id = tracking_id

    # Get user_id from JWT token
    try:
        verify_jwt_in_request(optional=True)
        
        # Retrieve `identity` (user_id) from the token
        user_id = get_jwt_identity()
        
        # Retrieve custom claims, including user_email
        jwt_claims = get_jwt()  # This will give you all claims in the token
        user_email = jwt_claims.get("email")  # Extract the `email` claim
        
        g.user_id = user_id
        g.user_email = user_email
        
    except Exception as e:
        print("Error retrieving user identity:", e)
        g.user_id = None
        g.user_email = None

   

@app.after_request
def add_tracking_id_cookie(response):
    
    """
    Add the trackingId cookie if it needs to be set.
    """
    if getattr(g, 'set_tracking_id_cookie', False):
        response.set_cookie('trackingId', g.tracking_id, httponly=True, secure=False, samesite='Lax')
    return response

from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt

        
@app.context_processor
def inject_has_token():
    has_token = False
    user_id = None
    user_email = None
    try:
        # Verify the JWT token from cookies
        verify_jwt_in_request(optional=True)
        
        # Retrieve `identity` (user_id) from the token
        user_id = get_jwt_identity()
        
        # Retrieve custom claims, including user_email
        jwt_claims = get_jwt()  # This will give you all claims in the token
        user_email = jwt_claims.get("email")  # Extract the `email` claim

        has_token = True if user_id else False
    except Exception as e:
        print("Error in JWT verification:", e)

    # Debug output
    print("Has token:", has_token)
    print("User ID:", user_id)
    print("User Email:", user_email)

    # Return variables available to templates
    return {
        'has_token': has_token,
        'user_id': user_id,
        'user_email': user_email
    }



@app.route('/')
def home():
    has_token = False
    user_id = None
    try:
        # Проверяваме за JWT токен в cookies
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()  # Вземаме идентификацията от токена
        if user_id:
            has_token = True
    except Exception as e:
        print(e)
        pass

    return render_template('index.html', has_token=has_token, user_id=user_id)


@app.route('/success')
@jwt_required()
def success():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400

    total_price = sum(item.quantity * item.product.price for item in cart_items)

    new_order = Order(user_id=user_id, total_price=total_price, status='Completed')
    db.session.add(new_order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)
        db.session.delete(item)

    db.session.commit()

    # Изпращане на имейл чрез smtplib

    return render_template('success.html', purchased_items=[], total_price=total_price)

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

@app.route('/cart')
def cart_page():
    return render_template('cart.html')


# Създаване на таблици в базата данни (по време на стартиране)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
