import unittest
from unittest.mock import MagicMock
from .models import models  

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.models= models()  


    def test_login_success(self):
        email = "test@example.com"
        password = "password"
        user = MagicMock()
        user.password = password
        user.query.filter_by.return_value.first.return_value = user

        with unittest.mock.patch('auth_service.User', user):
            success, message = self.auth_service.login(email, password)

        self.assertTrue(success)
        self.assertEqual(message, "Logged in successfully!")

    def test_login_failure(self):
        email = "test@example.com"
        password = "password"
        user = MagicMock()
        user.password = "wrong_password"
        user.query.filter_by.return_value.first.return_value = user

        with unittest.mock.patch('auth_service.User', user):
            success, message = self.auth_service.login(email, password)

        self.assertFalse(success)
        self.assertEqual(message, "Incorrect email or password.")

    def test_logout(self):
        message = self.auth_service.logout()
        self.assertEqual(message, "Logged out successfully.")

if __name__ == '__main__':
    unittest.main()
