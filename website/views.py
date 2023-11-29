'''
Main views of shop-easy app
'''

import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from student.inventory_details import get_inventory_details, \
    get_inventory_product
from student.cart import add_cart
from admin.inventory import add, update, delete
from student.cart import get_cart_details, get_user_inventory_details
from student.order import get_order_details, get_ordered_products, place_order, cancel_order

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/get-inventory', methods=['GET'])
@login_required
def get_inventory():
    try:
        inventory_products = get_inventory_details()
        if inventory_products:
            unique_categories = set(product.category for product in inventory_products)
            return render_template("get_inventory.html", products=inventory_products,
                                   categories=unique_categories)
        else:
            return render_template("get_inventory.html", products=[],
                                   categories=[])
    except Exception as e:
        logging.exception(e)

@views.route('admin/add-inventory', methods=['POST'])
@login_required
def add_inventory():
    name = request.form.get("name")
    description = request.form.get("description")
    quantity = int(request.form.get("quantity"))
    category = request.form.get("category")
    weight = int(request.form.get("weight"))
    expiry_date = datetime.strptime(request.form.get("expiry_date"), '%m-%d-%Y')
    print(f"Name: {name}, Description: {description}, Quantity: {quantity}, Category: {category}, Weight: {weight}, Expiry Date: {expiry_date}")
    # Validating the null check of input fields
    if any(value is None or value == "" for value in (name, description, quantity, category, weight, expiry_date)):
        flash("One or more form values are missing", category='error')
        return render_template("login.html", user=current_user)   
    else:
        status = add(name, description, quantity, category, weight, expiry_date)
        return redirect(url_for('views.get_inventory')) if status else render_template("login.html", user=current_user) #Redirect the else part to add_inventory html page 
    

@views.route('student/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    try:
        data = request.get_json()
        product_id = data.get('productId')
        quantity = data.get('quantity')
        add_cart(product_id,quantity)  
        return jsonify({'message': 'Item added to cart successfully'}), 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'Sorry! Unexpected error occured while adding the item to the cart'}), 500

@views.route('/cart', methods=['GET'])
@login_required
def get_cart():
    try:
        cart_details = get_cart_details(current_user)
        inventory_details = get_user_inventory_details(current_user)
        mapping_dict = {product.sku: product for product in cart_details}
        cart_products = [
            {"sku": product_details.sku,
            "name": product_details.name,
            "quantity": mapping_dict[product_details.sku].quantity}
            for product_details in inventory_details
            if product_details.sku in mapping_dict
        ]
        total_quantity = sum(product['quantity'] for product in cart_products)
        if cart_products:
            return render_template("checkout.html", cart_details=cart_products,
                                   total_quantity=total_quantity)
        flash("Cart is Empty !!", category='error')
        return render_template("checkout.html", cart_details=[],
                                   total_quantity=0)
    except Exception as e:
        logging.exception(e)
        return render_template("checkout.html", cart_details=[],
                                   total_quantity=0)


@views.route('/products', methods=['GET'])
@login_required
def get_products():
    try:
        inventory_products = get_inventory_details()
        if inventory_products:
            return render_template("products.html", products=inventory_products)
        else:
            return render_template("products.html", products=[])
    except Exception as e:
        logging.exception(e)

@views.route('/edit_product/<sku>', methods=['GET', 'POST'])
def edit_product(sku):
    
    product = get_inventory_product(sku)

    if request.method == 'POST':
        name = request.form.get("name")
        description = request.form.get("description")
        quantity = request.form.get("quantity")
        category = request.form.get("category")
        weight = request.form.get("weight")
        expiry_date = request.form.get("expiry_date")
        
        if any(value is None or value == "" for value in (name, description, quantity, category, weight, expiry_date)):
            flash("One or more form values are missing", category='error')
        else:
            status = update(product, name, description, quantity, category, weight, expiry_date)
            if status:
                flash("Product updated successfully !", category='success')
                return render_template('admin.html')
            else:
                flash("Product update failed !", category='error')
       
    return render_template('update_product.html', product=product)


@views.route('/delete_product/<sku>', methods=['DELETE'])
def delete_product(sku):

    product = get_inventory_product(sku)

    if product:
        status = delete(product)
        if status:
            flash("Product deleted successfully!", category='success')
            response_data = {'status': 'success', 'message': 'Product deleted successfully!'}
        else:
            flash("Product deletion failed!", category='error')
            response_data = {'status': 'error', 'message': 'Product deletion found'}
    else:
        flash("Product not found", category='error')
        response_data = {'status': 'error', 'message': 'Product not found'}
    
    return jsonify(response_data)

@views.route('/orders', methods=['GET'])
@login_required
def get_orders():
    try:
        order_details = get_order_details(current_user)
        products_ordered = get_ordered_products(order_details)
        if not products_ordered:
            flash("No order history available !!", category='success')
        return render_template('order.html', orders=products_ordered)
    except Exception as e:
        logging.exception(e)
        return render_template('order.html', orders=[])
    
@views.route('student/place-order', methods=['POST'])
@login_required
def order():
    try:
        data = request.get_json()
        place_order(data)  
        return jsonify({'message': 'Order placed successfully'}), 201
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'Sorry! Unexpected error occured while placing the order'}), 500



@views.route('student/cancel', methods=['PUT'])
@login_required
def cancel():
    try:
        order_id = request.get_json().get('order_id')
        print("OID:"+str(order_id))
        status = cancel_order(order_id)  
        if status:
            return jsonify({'message': 'Order cancelled successfully'}), 200
        else:
            return jsonify({'message': 'Sorry! Unable to cancel the order'}), 500
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'Sorry! Unexpected error occured while cancelling the order'}), 500
