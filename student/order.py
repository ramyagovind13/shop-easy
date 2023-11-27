'''
Order related function definitions
'''
import logging
from website.models import Order, db, OrderInventoryRelation
from flask_login import current_user

def place_order(data):

    try:      
        new_order = Order(
            user_id=current_user.user_id,
            units_sold=sum(item['quantity'] for item in data),
            order_status='Pending'  
        )      
        db.session.add(new_order)
        db.session.commit()
     
        for item in data:
            order_inventory_relation = OrderInventoryRelation(
                order_id=new_order.order_id,
                sku=item['sku'],
                quantity=item['quantity']
            )       
            db.session.add(order_inventory_relation)       
        db.session.commit()
        return True

    except Exception as e:      
        db.session.rollback()
        logging.exception(e)
        return False
    
    finally:
        db.session.close()