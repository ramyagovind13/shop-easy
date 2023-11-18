'''
Main views of shop-easy app
'''

import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from flask_mail import Mail, Message
from app import app 
from student.inventory_details import get_inventory_details
from student.cart import add_cart
from admin.inventory import add
from student.cart import get_cart_details, get_user_inventory_details
from flask_mail import Message
from datetime import dateti



views = Blueprint('views', __name__)
mail = Mail(app)

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
    data = request.get_json()
    product_id = data.get('productId')
    quantity = data.get('quantity')
    status = add_cart(product_id,quantity)  
    if status:
        return jsonify({'message': 'Item added to cart successfully'}), 200
    else:
        return jsonify({'message': 'Sorry! Unexpected error occured while adding the item to the cart'}), 500

def send_order_confirmation_email(email):
    try:
        msg = Message('Order Confirmation', recipients=[email])
        msg.body = 'Thank you for placing an order with Shop Easy. Your order has been successfully placed.'
        mail.send(msg)
        return True
    except Exception as e:
        logging.exception(e)
        return False


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
        else:
            flash("Cart is Empty !!", category='error')
            return render_template("checkout.html", cart_details=[],
                                   total_quantity=0)
    except Exception as e:
        logging.exception(e)

