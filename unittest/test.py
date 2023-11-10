import unittest
from website import app

class TestAuth(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_login_success(self):
        response = self.app.post('/login', data=dict(email='valid@test.com', password='password123'), follow_redirects=True)
        
        self.assertIn(b'Logged in successfully!', response.data)
        self.assertIn(b'Get Inventory Page', response.data)

    def test_login_failure(self):
        response = self.app.post('/login', data=dict(email='invalid@test.com', password='wrongpassword'), follow_redirects=True)
      
        self.assertIn(b'Sorry! Your email is not registered with Shop Easy.', response.data)
        self.assertIn(b'Login Page', response.data)

if __name__ == '__main__':
    unittest.main()
