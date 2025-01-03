from flask import Blueprint, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Order, OrderItem, CartItem, Product

order_bp = Blueprint('orders', __name__)

@order_bp.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    # Извличане на елементи от количката
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400

    # Изчисляване на общата сума
    total_price = sum(item.quantity * item.product.price for item in cart_items)

    # Създаване на поръчка
    new_order = Order(user_id=user_id, total_price=total_price, status='Pending')
    db.session.add(new_order)
    db.session.commit()  # За да получим валиден order_id

    # Прехвърляне на елементи в OrderItem
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        db.session.add(order_item)
        db.session.delete(cart_item)  # Изтриване на елемента от количката

    db.session.commit()  # Запис на всички промени

    return jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), 201


@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    # Извличане на поръчки
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()

    # Форматиране на резултата
    order_list = []
    for order in orders:
        order_items = [{
            'product_id': item.product_id,
            'quantity': item.quantity,
            'price': item.price,
            'total': item.quantity * item.price
        } for item in order.order_items]

        order_list.append({
            'id': order.id,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'total_price': order.total_price,
            'status': order.status,
            'items': order_items
        })

    return jsonify(order_list)


@order_bp.route('/', methods=['GET'])
@jwt_required()
def view_orders():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    # Retrieve orders for the current user
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()

    # Format orders
    order_list = [
        {
            'id': order.id,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'total_price': order.total_price,
            'status': order.status
        }
        for order in orders
    ]

    # Format items for each order
    order_items = [
        {
            'order_id': item.order_id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.price,
            'total': item.quantity * item.price
        }
        for order in orders
        for item in order.order_items
    ]

    return render_template('orders.html', orders=order_list, items=order_items)
