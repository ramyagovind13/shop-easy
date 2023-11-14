import logging
from flask import flash
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user
from student.auth import can_student_login
from website.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            if user.password == password :
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.get_inventory'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Sorry! Your email is not registered with Shop Easy.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

