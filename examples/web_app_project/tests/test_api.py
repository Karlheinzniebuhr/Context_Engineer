import unittest
import json
from app import app, db, User, Metric

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create test user
            user = User(name='Test User', email='test@example.com')
            db.session.add(user)
            db.session.commit()
            self.test_user_id = user.id
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_user(self):
        response = self.client.get(f'/api/users/{self.test_user_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test User')
        self.assertEqual(data['email'], 'test@example.com')
    
    def test_get_nonexistent_user(self):
        response = self.client.get('/api/users/999')
        self.assertEqual(response.status_code, 404)
    
    def test_create_user(self):
        user_data = {
            'name': 'New User',
            'email': 'newuser@example.com'
        }
        
        response = self.client.post('/api/users', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New User')
        self.assertEqual(data['email'], 'newuser@example.com')
    
    def test_create_metric(self):
        metric_data = {
            'user_id': self.test_user_id,
            'name': 'test_metric',
            'value': 123.45
        }
        
        response = self.client.post('/api/metrics',
                                  data=json.dumps(metric_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'test_metric')
        self.assertEqual(data['value'], 123.45)
    
    def test_get_metrics(self):
        # First create a metric
        with self.app.app_context():
            metric = Metric(user_id=self.test_user_id, name='test_metric', value=100.0)
            db.session.add(metric)
            db.session.commit()
        
        response = self.client.get(f'/api/metrics/{self.test_user_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'test_metric')
        self.assertEqual(data[0]['value'], 100.0)

if __name__ == '__main__':
    unittest.main()
