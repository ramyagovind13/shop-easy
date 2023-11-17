from flask import flash
from flask_login import login_user

def can_admin_login(password, user, role):
    if user.check_password(password):
        flash('Logged in successfully!', category='success')
        login_user(user, remember=True)
        return True
    else:
        flash('Incorrect password, try again.', category='error')
    return False
