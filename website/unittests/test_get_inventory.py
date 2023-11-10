import unittest
from unittest.mock import patch
from website import app

class TestGetInventory(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('website.views.render_template')
    @patch('website.views.get_inventory_details')
    @patch('website.views.current_user')
    def test_get_inventory_allowed_only_when_user_is_authenticated(
        self, mock_current_user, mock_get_inventory_details, mock_render_template):

        mock_current_user.is_authenticated = True
        response = self.app.get('/get-inventory')

        self.assertEqual(response.status_code, 200)
        mock_get_inventory_details.assert_called_once()
        mock_render_template.assert_called_once()


    @patch('website.views.render_template')
    @patch('website.views.get_inventory_details')
    @patch('website.views.current_user')
    def test_get_inventory_is_not_allowed_when_user_is_not_authenticated(
        self, mock_current_user, mock_get_inventory_details, mock_render_template):

        mock_current_user.is_authenticated = False
        response = self.app.get('/get-inventory')

        self.assertEqual(response.status_code, 200)
        mock_get_inventory_details.assert_not_called()
        mock_render_template.assert_called_once_with('login.html')

    @patch('website.views.render_template')
    @patch('website.views.get_inventory_details')
    @patch('website.views.current_user')
    def test_get_inventory_product_details(
        self, mock_current_user, mock_get_inventory_details, mock_render_template):

        mock_current_user.is_authenticated = True
        mock_get_inventory_details.return_value = ['Apple', 'Tomato']

        response = self.app.get('/get-inventory')

        content = response.get_data(as_text=True)
        self.assertIn('Apple', content)
        self.assertIn('Tomato', content)

        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_once_with('get_inventory.html',
                                                      products=['Apple', 'Tomato'])

    @patch('website.views.render_template')
    @patch('website.views.get_inventory_details')
    @patch('website.views.current_user')
    def test_get_inventory_throws_exception(
        self, mock_current_user, mock_get_inventory_details, mock_render_template):

        mock_current_user.is_authenticated = True
        mock_get_inventory_details.side_effects = Exception('Connection error')

        with self.assertRaises(Exception):
            self.app.get('/get-inventory')
        mock_render_template.assert_not_called()


if __name__ == '__main__':
    unittest.main()


