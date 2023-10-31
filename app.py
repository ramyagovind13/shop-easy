from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user
from werkzeug.datastructures import MultiDict  #updated import

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def home():
    return "home" 

@app.route('/Userlogin', methods=['GET'])
def Userlogin(request):
    args = MultiDict(request.args) # Use MultiDict to replace url_decode
    # your login logic using 'args' here
    return render_template('login.html')
    a=request.getusername
    b=request.getpassword()

    record.password =b 
    return login 
    

if __name__ == "__main__":
    app.run(debug=True , port= 5433)    