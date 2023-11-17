import logging
from flask import flash
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user
from student.auth import can_student_login
from admin.auth import can_admin_login
from website.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:   
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user:
                if user.role == "student":
                    if(can_student_login(password,user)):
                        return redirect(url_for('views.get_inventory'))
                    else:  
                        if user.role == "admin":
                            if (can_admin_login(password, user)):                            
                                 return redirect(url_for('views.get_inventory'))      
            else:
                flash('Sorry! Your email is not registered with Shop Easy.', category='error')         
        return render_template("login.html", user=current_user)     
    except Exception as e:
        logging.exception(e)
        flash('An unexpected error occurred. Please try again later.', category='error')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))