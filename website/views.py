'''
Main views of shop-easy app
'''

import logging
from flask import Blueprint, render_template
from flask_login import login_required

from student.inventory_details import get_inventory_details
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
