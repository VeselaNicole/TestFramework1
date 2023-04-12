import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserRegister(BaseCase):

    def setup_method(self):
        base_part = 'Nicole'
        domain = 'example.com'
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '1234',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'username': 'learnqa',
            'email': self.email
        }
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_json_value_by_key(response, "id")
        Assertions.assert_status_code(response, 200)

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '1234',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'username': 'learnqa',
            'email': email
        }
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists"
    def test_create_user_with_incorrect_email(self):
        email_without_at = self.email.replace("@", "")
        data = {
            'password': '1234',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'username': 'learnqa',
            'email': email_without_at
        }
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, 'Invalid email format')