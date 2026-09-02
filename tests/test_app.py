import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_about_status_code(self):
        result = self.app.get('/about')
        self.assertEqual(result.status_code, 200)

    def test_api_history(self):
        result = self.app.get('/api/history')
        self.assertEqual(result.status_code, 200)
        self.assertTrue(isinstance(result.get_json(), list))

    def test_api_reset_history(self):
        result = self.app.post('/api/reset-history')
        self.assertEqual(result.status_code, 200)
        data = result.get_json()
        self.assertEqual(data.get('status'), 'success')

    def test_predict_success(self):
        form_data = {
            'name': 'John Doe',
            'gender': 'Male',
            'age': '45',
            'height': '175',
            'weight': '75',
            'sleep_hours': '7',
            'bp_systolic': '120',
            'bp_diastolic': '80',
            'heart_rate': '72',
            'temperature': '36.6',
            'blood_sugar': '95',
            'cholesterol': '180',
            'diet': 'Good',
            'exercise_level': 'Medium',
            'stress': 'Low',
            'smoking': 'No',
            'alcohol': 'Low',
            'family_history': 'No',
            'existing_diseases': '',
            'symptoms': 'None'
        }
        result = self.app.post('/predict', data=form_data)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Diagnostic Assessment Result', result.data)
        self.assertIn(b'John Doe', result.data)
        self.assertIn(b'7 hrs/night', result.data)

    def test_predict_invalid_input(self):
        form_data = {
            'name': 'John Doe',
            'age': '-5', # Invalid age
            'height': '175',
            'weight': '75'
        }
        result = self.app.post('/predict', data=form_data)
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid Input', result.data)

    def test_predict_invalid_method(self):
        result = self.app.get('/predict')
        self.assertEqual(result.status_code, 405)

    def test_404_handler(self):
        result = self.app.get('/nonexistent-page')
        self.assertEqual(result.status_code, 404)
        self.assertIn(b'Page Not Found', result.data)

if __name__ == '__main__':
    unittest.main()
