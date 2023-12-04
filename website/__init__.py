from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Adarsh123#@localhost:5432/shop_easy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy modification tracking
    app.config['MAIL_SERVER'] = 'smtp.mailgun.org'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'postmaster@sandbox9ce539941dc343e5b7ee78b28bee361b.mailgun.org'
    app.config['MAIL_PASSWORD'] = '88118e3cffc1fd3c8b910b5f6635d472-0a688b4a-02d5b91e'
    app.config['MAIL_DEFAULT_SENDER'] = 'postmaster@sandbox9ce539941dc343e5b7ee78b28bee361b.mailgun.org'


    db.init_app(app)
    mail.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
        
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
         
    with app.app_context():
        db.create_all()

    return app