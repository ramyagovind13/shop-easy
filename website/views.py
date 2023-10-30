'''
Main views of shop-easy app
'''

from flask import Blueprint
views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to shop-easy app !!</h1>"