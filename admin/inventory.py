import logging
from flask import flash
from website.models import Inventory, db

def add(name, description, quantity, category, weight, expiry_date):
    try:
        
        # Creating an instance of the inventory class

        new_inventory =  Inventory(
        name=name,
        description=description,
        quantity=quantity,
        category=category,
        weight=weight,
        expiry_date=expiry_date
        )

        # Adding the instance to the database session and commiting the changes 
                     
        db.session.add(new_inventory)
        db.session.commit()   
        flash('Inventory added successfully!', category='success') 
        return True
    except Exception as e:
        logging.exception(e)
        flash("Sorry! Unable to add the Inventory", category='error')
        return False
    
def update(product, name, description, quantity, category, weight, expiry_date):
    try:
        product.name = name
        product.description = description
        product.quantity = quantity
        product.category = category
        product.weight = weight
        product.expiry_date = expiry_date
        db.session.add(product)
        db.session.commit()   
        return True
    except Exception as e:
        logging.exception(e)
        return False
    
def delete(product):
    try:
        db.session.delete(product)
        db.session.commit()
        return True
    except Exception as e:
        logging.exception(e)
        return False