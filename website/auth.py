from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password :
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                print('Incorrect password, try again.', category='error')
        else:
            print('Sorry! Your email is not registered with Shop Easy.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

