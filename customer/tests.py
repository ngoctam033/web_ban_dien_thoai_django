from django.test import TestCase, Client
from django.urls import reverse

class CustomerViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_payload = {
            'name': 'John',
            'email': 'john@example.com',
            'password': 'password',
            'address': '123 Main St'
        }
        self.invalid_payload = {
            'name': '',
            'email': 'john@example',
            'password': 'password',
            'address': '123 Main St'
        }

    def test_post_customer(self):
        response = self.client.post(reverse('create_customer'), data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Account created successfully."})

    def test_post_customer_invalid(self):
        response = self.client.post(reverse('create_customer'), data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message": "Account creation failed."})