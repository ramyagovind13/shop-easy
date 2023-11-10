import unittest
from flask import Flask
from flask_testing import TestCase
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from website import app, db
from website.models import User
from website.auth import auth

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['WTF_CSRF_ENABLED'] = False
app.register_blueprint(auth)
login_manager = LoginManager(app)
login_manager.init_app(app)


class TestAuth(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_successful(self):
        test_user = User(email='test@example.com', password=generate_password_hash('password'), role='user')
        db.session.add(test_user)
        db.session.commit()

        response = self.client.post('/login', data=dict(username='test@example.com', password='password'))

        self.assertRedirects(response, url_for('views.admin'))

        with self.client.session_transaction() as session:
            flash_messages = session['_flashes']
            self.assertIn(('Logged in successfully!', 'success'), flash_messages)

    def test_login_incorrect_password(self):
        test_user = User(email='test@example.com', password=generate_password_hash('password'), role='user')
        db.session.add(test_user)
        db.session.commit()

        response = self.client.post('/login', data=dict(username='test@example.com', password='wrong_password'))

        self.assertTemplateUsed('login.html')

        with self.client.session_transaction() as session:
            flash_messages = session['_flashes']
            self.assertIn(('Incorrect password, try again.', 'error'), flash_messages)

    def test_login_unregistered_email(self):

        response = self.client.post('/login', data=dict(username='nonexistent@example.com', password='password'))

        self.assertTemplateUsed('login.html')

        with self.client.session_transaction() as session:
            flash_messages = session['_flashes']
            self.assertIn(('Sorry! Your email is not registered with Shop Easy.', 'error'), flash_messages)

    def test_logout(self):

        self.client.post('/login', data=dict(username='test@example.com', password='password'))

        response = self.client.get('/logout')

        self.assertRedirects(response, url_for('auth.login'))

        with self.client.session_transaction() as session:
            self.assertNotIn('user_id', session)

if __name__ == '__main__':
    unittest.main()
