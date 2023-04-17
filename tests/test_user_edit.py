import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        #Register User
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_value_by_key(response1, "id")

        email = register_data["email"]
        firstName = register_data["firstName"]
        lastName = register_data["lastName"]
        password = register_data["password"]
        username = register_data["username"]

        user_id = self.get_json_value(response1, "id")

        #Login
        login_data = {
            "email": email,
            "password": password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
