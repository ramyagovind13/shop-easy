from website.models import Inventory

def get_inventory_details():
    inventory_products = Inventory.query.all()
    return inventory_products
