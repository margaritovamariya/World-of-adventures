from flask import Blueprint, g, request, jsonify, render_template, redirect, url_for, flash, make_response
from extensions import db, bcrypt
from models import CartItem, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth = Blueprint('auth', __name__)

# Регистрация
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.register'))

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('auth.register'))

        # Hash the password and create a new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Associate cart items with the new user
        tracking_id = getattr(g, 'tracking_id', None)
        if tracking_id:
            # Update all cart items with the current tracking_id
            CartItem.query.filter_by(tracking_id=tracking_id).update({'user_id': new_user.id})
            db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('login.html', show_register=True)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Получаване на данни от формата
        email = request.form['email']
        password = request.form['password']

        # Проверка за съществуващ потребител
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # Генериране на JWT токен
            access_token = create_access_token(identity=str(user.id),  # The `identity` remains the `user_id`
    additional_claims={"email": user.email},  # Add `user_email` as a custom claim
    expires_delta=timedelta(hours=24))

            # Създаване на отговор и задаване на токена в cookies
            response = make_response(redirect(url_for('home')))  # Пренасочване към началната страница
            response.set_cookie('access_token', access_token, httponly=True, secure=False)  # secure=True при HTTPS
            flash('Welcome back!', 'success')
            return response

        # Грешка при невалиден email или парола
        flash('Invalid email or password!', 'danger')
        return redirect(url_for('auth.login'))

    # Обработка на GET заявката (зареждане на формуляра за вход)
    return render_template('login.html')

@auth.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('auth.login')))
    response.delete_cookie('access_token')
    flash('Logged out successfully!', 'success')
    return response


# Примерен защитен маршрут
@auth.route('/protected', methods=['GET'])
@jwt_required()
def protection():
    current_user = get_jwt_identity()  # Извличаме ID на текущия потребител от токена
    return jsonify({"message": f"Hello, user with ID {current_user}!"}), 200
