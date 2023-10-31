from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user
from werkzeug.datastructures import MultiDict  #updated import

app = Flask(__name__)
db = SQLAlchemy(app)