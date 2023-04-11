import pytest
import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookies"),
        ("no_headers")
    ]

    def setup_method(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")

        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_user_auth(self):

        response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response2, "user_id", self.user_id_from_auth_method,
                                             "user id from auth method is not equal to user_id in check method")

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth(self, condition):

        if condition == 'no_cookies':
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     headers={"x-csrf-token": self.token})

        else:
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response2, "user_id", 0, f"user is authorized with condition {condition}")
