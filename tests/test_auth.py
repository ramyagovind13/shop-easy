import unittest
import sys
import os
sys.path.append(os.path.abspath('/Users/chethu/Repo/shop-easy'))
from flask import url_for
from flask_testing import TestCase
from app import create_app
from website import db  # Update import statement
from website.models import User  # Update import statement


class TestAuthRoutes(TestCase):

    def create_app(self):
        # Use the create_app function from the __init__.py file
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///:memory:' 
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        return app

    def setUp(self):
        # Create tables in the PostgreSQL database
        with self.app.app_context():
            db.create_all()

        # Create a test user
        test_user = User(email='test@example.com', password='test_password')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        # Drop all tables after each test
        db.session.remove()
        db.drop_all()

    def test_login_success(self):
        with self.client:
            response = self.client.post(
                url_for('auth.login'),
                data={'email': 'test@example.com', 'password': 'test_password'},
                follow_redirects=True
            )
            self.assertIn(b'Logged in successfully!', response.data)
            self.assertEqual(response.status_code, 200)

    def test_login_incorrect_password(self):
        with self.client:
            response = self.client.post(
                url_for('auth.login'),
                data={'email': 'test@example.com', 'password': 'incorrect_password'},
                follow_redirects=True
            )
            self.assertIn(b'Incorrect password, try again.', response.data)
            self.assertEqual(response.status_code, 200)
    
    def test_login_unregistered_email(self):
        with self.client:
            response = self.client.post(
                url_for('auth.login'),
                data={'email': 'nonexistent@example.com', 'password': 'test_password'},
                follow_redirects=True
            )
            self.assertIn(b'Sorry! Your email is not registered with Shop Easy.', response.data)
            self.assertEqual(response.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()
