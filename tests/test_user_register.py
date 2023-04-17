import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserRegister(BaseCase):
    exclude_params = [
        ("no_password"),
        ("no_firstName"),
        ("no_lastName"),
        ("no_username"),
        ("no_email")
    ]

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
        print(response.content)

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

    @pytest.mark.parametrize("condition", exclude_params)
    def test_create_user_without_field(self, condition):
        expected_result = f"The following required params are missed: {condition[3:]}"
        if condition == "no_password":
            data = {
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'username': 'learnqa',
                'email': self.email
            }
        if condition == "no_firstName":
            data = {
                'password': '1234',
                'lastName': 'learnqa',
                'username': 'learnqa',
                'email': self.email
            }
        if condition == "no_lastName":
            data = {
                'password': '1234',
                'firstName': 'learnqa',
                'username': 'learnqa',
                'email': self.email
            }

        if condition == "no_username":
            data = {
                'password': '1234',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': self.email
            }

        if condition == "no_email":
            data = {
                'password': '1234',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'username': 'learnqa'
            }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, expected_result)


    def test_username_min_length(self):
        short_username = "n"
        data = {
            'password': '1234',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'username': short_username,
            'email': self.email
        }
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "The value of 'username' field is too short")


    def test_username_max_length(self):


        username_max_length = 250
        long_username = self.generate_long_username(username_max_length)
        data = {
            'password': '1234',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'username': long_username,
            'email': self.email
        }
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "The value of 'username' field is too long")