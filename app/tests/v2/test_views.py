""" Test cases for views.py """

import unittest
import json
from app import create_app
from app.api.v2.models import DatabaseManager, UserOps


class TestHomePage(unittest.TestCase):
    """ Test Routes """
    def setUp(self):
        """ Instantiate test client """
        self.app = create_app(config_mode='testing')
        self.app = self.app.test_client()

    def test_index_status_code(self):
        """Test for home page data"""
        test_resp = self.app.get(
            '/api/v2/',
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(test_resp.status_code, 200)
        self.assertNotEqual(test_resp.status_code, 404)

    def test_index_output_data(self):
        """Test for home page status code 200(ok)"""
        test_resp = self.app.get(
            '/api/v2/',
            headers={'content-type': 'application/json'}
        )

        self.assertIn(b"Welcome User", test_resp.data, msg="Homepage message")

    

class TestUserOpsRoute(unittest.TestCase):
    """ Test route to register new user """
    def setUp(self):
        """ Instantiate test client with data """
        self.app = create_app(config_mode='testing')
        self.app = self.app.test_client()
        self.sample_reg_info = {
            'username': 'mrnonamee',
            'email': 'mrnoname@email.com',
            'password': 'elephantman',
            'name': 'Arthur Ngondo',
        }

        # DatabaseManger.create_all_tables()
         
    def tearDown(self):
        pass
    
    def test_payload_before_posting(self):
        """ Test that function checks that data from model conforms with
            requirements before deploying the payload
        """
        test_resp = self.app.post(
            '/api/v2/auth/signup',
            data=json.dumps('I want to register'),
            headers={'content-type': 'application/json'}
        )
        self.assertIn(b"Sorry.... the provided data is malformed", test_resp.data)

    def test_post_orders_status_code(self):
        """ Test that valid path and data for successful user creation
            returns HTTP status 201 
        """
        test_resp = self.app.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.sample_reg_info),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(test_resp.status_code, 201)
        self.assertNotEqual(test_resp.status_code, 405)
        self.assertNotEqual(test_resp.status_code, 404)
        self.assertNotEqual(test_resp.status_code, 400)
        self.assertIn(b"Successfully registered", test_resp.data)

    def test_post_orders_operational_message(self):
        """ Test that valid path and data for successful user creation
            returns a custom message to indicate success a valid auth token and content type
        """
        test_resp = self.app.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.sample_reg_info),
            headers={'content-type': 'application/json'}
        )
        data = json.loads(test_resp.data.decode())
        self.assertTrue(data["Status"] == "Success")
        self.assertTrue(data["Message"] == "Registration successful")
        self.assertTrue(data["Authentication token"])
        self.assertTrue(test_resp.content_type == 'application/json')

