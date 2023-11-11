from models import User
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user

class AuthService:
    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user, remember=True)
            return True, "Logged in successfully!"
        else:
            return False, "Incorrect email or password."

    @staticmethod
    def logout():
        logout_user()
        return "Logged out successfully."


auth = Blueprint('auth', __name__)
auth_service = AuthService()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        success, message = auth_service.login(email, password)
        if success:
            flash(message, category='success')
            return redirect(url_for('views.admin'))
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