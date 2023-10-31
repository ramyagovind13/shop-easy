from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.datastructures import MultiDict  #updated import

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

# In a production application, user data would be stored in a database
# Here, we use a simple dictionary as a database for demonstration purposes
users = {'admin_user': {'password': 'admin_password'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def home():
    return 'Welcome to the homepage'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and password == users[username]['password']:
            user = User(username)
            login_user(user)
            return redirect(url_for('admin'))
    
    return render_template('login.html')

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    return 'Welcome to the admin panel'

if __name__ == '__main__':
    app.run(debug=True, port=5433)    




