'''
Main views of shop-easy app
'''

import logging
from flask import Blueprint, render_template
from flask_login import current_user

from student.inventory_details import get_inventory_details
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/get-inventory', methods=['GET'])
def get_inventory():
    try:
        if current_user.is_authenticated:
            inventory_products = get_inventory_details()
            return render_template("get_inventory.html", products=inventory_products)
        else:
            return render_template("login.html")
    except Exception as e:
        logging.exception(e)
