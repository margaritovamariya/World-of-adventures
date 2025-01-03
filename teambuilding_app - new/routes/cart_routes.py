from flask import Blueprint, request, jsonify, redirect, g
from extensions import db
from models import CartItem, Product

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    tracking_id = getattr(g, 'tracking_id', None)
    user_id = getattr(g, 'user_id', None)
    
    print('huq')
    print(tracking_id)
    print(user_id)

    cart_item = CartItem(product_id=product.id, quantity=1, tracking_id=tracking_id, user_id=user_id)
    db.session.add(cart_item)
    db.session.commit()

    return jsonify({'message': f'Added {product.name} to cart'}), 201

@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    tracking_id = getattr(g, 'tracking_id', None)
    user_id = getattr(g, 'user_id', None)
    
    print(tracking_id, user_id)
    
    # Fetch cart items based on user_id or tracking_id
    if user_id:
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
    elif tracking_id:
        cart_items = CartItem.query.filter_by(tracking_id=tracking_id).all()
    else:
        return jsonify({'error': 'No tracking ID or user ID found'}), 400
    
    print(cart_items)

    # Prepare the response data
    cart_data = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            cart_data.append({
                'product_id': item.product_id,
                'name': product.name,
                'price': product.price,
                'quantity': item.quantity,
                'total': product.price * item.quantity
            })

    return jsonify(cart_data)


@cart_bp.route('/cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    tracking_id = getattr(g, 'tracking_id', None)
    user_id = getattr(g, 'user_id', None)

    # Filter by user_id or tracking_id
    if user_id:
        cart_item = CartItem.query.filter_by(product_id=product_id, user_id=user_id).first()
    elif tracking_id:
        cart_item = CartItem.query.filter_by(product_id=product_id, tracking_id=tracking_id).first()
    else:
        return jsonify({'error': 'No tracking ID or user ID found'}), 400

    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': f'Product removed from cart successfully'}), 200

@cart_bp.route('/cart/<int:product_id>/increase', methods=['POST'])
def increase_quantity(product_id):
    tracking_id = getattr(g, 'tracking_id', None)
    user_id = getattr(g, 'user_id', None)

    # Filter by user_id or tracking_id
    if user_id:
        cart_item = CartItem.query.filter_by(product_id=product_id, user_id=user_id).first()
    elif tracking_id:
        cart_item = CartItem.query.filter_by(product_id=product_id, tracking_id=tracking_id).first()
    else:
        return jsonify({'error': 'No tracking ID or user ID found'}), 400

    if not cart_item:
        return jsonify({'error': 'Product not found in cart'}), 404

    cart_item.quantity += 1
    db.session.commit()

    return jsonify({'message': 'Quantity increased successfully'})

@cart_bp.route('/cart/<int:product_id>/decrease', methods=['POST'])
def decrease_quantity(product_id):
    tracking_id = getattr(g, 'tracking_id', None)
    user_id = getattr(g, 'user_id', None)

    # Filter by user_id or tracking_id
    if user_id:
        cart_item = CartItem.query.filter_by(product_id=product_id, user_id=user_id).first()
    elif tracking_id:
        cart_item = CartItem.query.filter_by(product_id=product_id, tracking_id=tracking_id).first()
    else:
        return jsonify({'error': 'No tracking ID or user ID found'}), 400

    if not cart_item:
        return jsonify({'error': 'Product not found in cart'}), 404

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        db.session.commit()
        return jsonify({'message': 'Quantity decreased successfully'})
    else:
        # If quantity is 1, remove the item from the cart
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Product removed from cart'})
