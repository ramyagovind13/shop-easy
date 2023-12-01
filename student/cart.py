'''
Student Cart related function definitions
'''

import logging
from website.models import Cart, db, InvetoryCartRelation
from flask_login import current_user

def add_cart(product_id, quantity):
    try:

        existing_user_cart_relation = Cart.query.filter_by(user_id=current_user.user_id).first()
        print("Fetched Existing cart relation")
        if not existing_user_cart_relation:
            cart = Cart(user_id=current_user.user_id)
            db.session.add(cart)
            db.session.commit()
        print("Added user relation to the cart")
        # Get the cart ID for the current user
        cart_record = Cart.query.filter_by(user_id=current_user.user_id).first()

        # Check if the item is already in the cart
        existing_relation = InvetoryCartRelation.query.filter_by(cart_id=cart_record.cart_id, sku=product_id).first()
        print("Existing relation check done")
        if existing_relation:
            # If the item is already in the cart, update the quantity
            existing_relation.quantity += int(quantity)
        else:
            # If the item is not in the cart, create a new relation
            inventoty_cart= InvetoryCartRelation(cart_id=cart_record.cart_id, sku=product_id, quantity=quantity)
            db.session.add(inventoty_cart)

        db.session.commit()
        print("Added to cart successfully")
    except Exception as e:
        logging.exception(e)
        print("Sorry! Unable to add the Inventory")


def get_cart_details(current_user):
    try:
        user_cart = current_user.carts
        cart_id = user_cart[0].cart_id
        if cart_id:
            cart_details = InvetoryCartRelation.query.filter_by(cart_id=cart_id).all()
        return cart_details
    except Exception as e:
        logging.exception(e)
        return None
    
def get_user_inventory_details(current_user):
    user_cart = current_user.carts
    inventory_details = user_cart[0].inventory
    return inventory_details


def clear_cart(current_user):
    try:
        user_cart = current_user.carts
        cart_id = user_cart[0].cart_id
        if cart_id:
            cart_details = InvetoryCartRelation.query.filter_by(cart_id=cart_id).all()
            for detail in cart_details:
                db.session.delete(detail)

            db.session.delete(user_cart[0])
            db.session.commit()
            return True
    except Exception as e:
        logging.exception(e)
        return None