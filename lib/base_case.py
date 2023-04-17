import json.decoder
import requests
from datetime import datetime

from requests import Response


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name '{cookie_name}' in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Cannot find header with name '{header_name}' in the last response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response in not in JSON format. Response text is '{response.text}"
        assert name in response_as_dict, f"Response JSON doesn't have field '{name}'"
        return response_as_dict[name]

    def generate_long_username(self, max_allowed_length):
        long_username = ""
        while len(long_username) <= max_allowed_length:
            long_username += "a"

        return long_username

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = 'Nicole'
            domain = 'example.com'
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '1234',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'username': 'learnqa',
            'email': email
        }

    def create_user_and_auth(self):
        # Register User
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        email = register_data["email"]
        firstName = register_data["firstName"]
        lastName = register_data["lastName"]
        password = register_data["password"]
        username = register_data["username"]

        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            "email": email,
            "password": password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        result = dict()
        result["user_id"] = user_id
        result["auth_sid"] = auth_sid
        result["x-csrf-token"] = token
        result["email"] = email
        result["firstName"] = firstName

        return result

