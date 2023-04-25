import allure
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Get user info tests")
class TestGetUser(BaseCase):

    @allure.title("Get user info being unauthorized")
    @pytest.mark.smoke_test
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_unauthorised(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_value_by_key(response, "username")
        Assertions.assert_json_value_has_no_key(response, "email")
        Assertions.assert_json_value_has_no_key(response, "lastName")
        Assertions.assert_json_value_has_no_key(response, "firstName")

    @allure.issue('222', "No email in response")
    @allure.title("Get full info by authorized user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_auth_with_same_id(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        expected_fields = ["username", "email", "lastName", "firstName"]
        Assertions.assert_json_value_by_keys(response2, expected_fields)

    @allure.title("get info about user being authorized by another user")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_user_auth_with_different_id(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Register Another user to get id
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post('/user/', data=register_data)
        other_user_id = self.get_json_value(response2, "id")

        response3 = MyRequests.get(f"/user/{other_user_id}",
                                   headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        unexpected_fields = ["email", "lastName", "firstName"]
        Assertions.assert_json_value_by_key(response3, "username")
        Assertions.assert_json_has_no_keys(response3, unexpected_fields)
