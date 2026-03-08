import unittest
from app import app, db

class TodoAPITestCase(unittest.TestCase):
    # setUp() runs automatically BEFORE every single test
    def setUp(self):
        app.config['TESTING'] = True

        # this is very important step. You are creating a db in the RAM
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    # Any function that we write that starts with test_ will be run by python

    def test_user_registration(self):
        mock_data = {
            "username": "test@example.com",
            "password": "securepassword123"
        }

        response = self.client.post('/register', json=mock_data)

        # 3. Assert

        status_code = response.status_code
        data = response.get_json()

        self.assertIn('message', data.keys())
        self.assertEqual(status_code, 201)
    
    def test_get_todos(self):
        mock_data = {
            "username": "test@example.com",
            "password": "securepassword123"
        }
        self.client.post('/register', json=mock_data)
        response = self.client.post('/login', json=mock_data)
        access_token = response.get_json().get('access_token')

        response = self.client.get('/todos', headers={
            'Authorization' : f'Bearer {access_token}'
        })

        data = response.get_json()

        self.assertIn('data',data.keys())
        self.assertIn('page',data.keys())
        self.assertIn('limit',data.keys())
        self.assertIn('total',data.keys())
        self.assertEqual(response.status_code, 200)