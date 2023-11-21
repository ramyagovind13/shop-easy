from flask_mail import Message
from datetime import datetime
import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import mail  # Import the mail instance from the package

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

# ... (your existing routes)

@views.route('/place-order', methods=['POST'])
@login_required
def place_order():
    try:
        # ... (existing code to handle order placement)

        # Send email notification to the user
        send_order_confirmation_email(current_user.email)

        flash('Order placed successfully! Check your email for confirmation.', category='success')
        return redirect(url_for('views.home'))

    except Exception as e:
        logging.exception(e)
        flash('An unexpected error occurred. Please try again later.', category='error')
        return render_template("place_order.html", user=current_user)

def send_order_confirmation_email(email):
    try:
        msg = Message('Order Confirmation', recipients=[email])
        msg.body = 'Thank you for placing an order with Shop Easy. Your order has been successfully placed.'
        mail.send(msg)
        return True

    except Exception as e:
        logging.exception(e)
        return False
