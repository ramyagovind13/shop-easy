'''
Main views of shop-easy app
'''

import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from student.inventory_details import get_inventory_details
from admin.inventory import add
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/get-inventory', methods=['GET'])
@login_required
def get_inventory():
    try:
        inventory_products = get_inventory_details()
        print(inventory_products)
        return render_template("get_inventory.html", products=inventory_products)
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
    if None or "" in (name, description, quantity, category, weight, expiry_date):
        flash("One or more form values are missing", category='error')
        return render_template("login.html", user=current_user) #Redirect the URL to add_inventory html page
    else:
        status = add(name, description, quantity, category, weight, expiry_date)
        return redirect(url_for('views.get_inventory')) if status else render_template("login.html", user=current_user) #Redirect the else part to add_inventory html page 
    
    
    
        

