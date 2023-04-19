

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests

class TestUserDelete(BaseCase):
    def test_delete_protected_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        response2 = MyRequests.delete(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_response_content(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    def test_delete_new_user(self):
        new_user_data = self.create_user_and_auth()
        user_id = new_user_data["user_id"]
        auth_sid = new_user_data["auth_sid"]
        token = new_user_data["x-csrf-token"]
        response1 = MyRequests.delete(f"/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response1, 200)

        response2 = MyRequests.get(f"/user/{user_id}",
                                 headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_status_code(response2, 404)
        Assertions.assert_response_content(response2, "User not found")


    def test_delete_another_user(self):
        login_user_data = self.create_user_and_auth()
        auth_sid = login_user_data["auth_sid"]
        token = login_user_data["x-csrf-token"]
        user_id1 = login_user_data["user_id"]

        delete_user_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=delete_user_data)

        user_id2 = self.get_json_value(response1, "id")

        response2 = MyRequests.delete(f"/user/{user_id2}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_status_code(response2, 200)

        response3 = MyRequests.get(f"/user/{user_id2}")
        Assertions.assert_json_value_by_key(response3, "username")