import logging
from flask import flash
from website.models import Inventory, db

def add(name, description, quantity, category, weight, expiry_date):
    try:
        new_inventory =  Inventory(
        name=name,
        description=description,
        quantity=quantity,
        category=category,
        weight=weight,
        expiry_date=expiry_date
        )               
        db.session.add(new_inventory)
        db.session.commit()   
        flash('Inventory added successfully!', category='success') 
        return True
    except Exception as e:
        logging.exception(e)
        flash("Sorry! Unable to add the Inventory", category='error')
        return False
    