from unittest import TestCase
from blog.routes import index
from blog import app


class RouteTests(TestCase):

    # Test index route
    def test_index_route(self):

        with app.test_client() as tc:

            response = tc.get('/')
            redirect_response = tc.get('/home')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(redirect_response.status_code, 200)

    # Test about page route
    def test_about_route(self):

        with app.test_client() as tc:

            response = tc.get('/about')
            self.assertEqual(response.status_code, 200)

    # Test user registration route
    def test_registration_route(self):

        with app.test_client() as tc:

            response = tc.get('/register')
            self.assertEqual(response.status_code, 200)

    # Test user login route
    def test_login_route(self):

        with app.test_client() as tc:

            response = tc.get('/login')
            self.assertEqual(response.status_code, 200)