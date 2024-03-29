from flaky import flaky
import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Edit tests")
class TestUserEdit(BaseCase):
    @allure.title("Creates new user, authorizes with it, updates the first name and check the final result")
    @pytest.mark.new_feature
    def test_edit_just_created_user(self):
        #Register User
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

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
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #edit

        new_name = "changed name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})


        Assertions.assert_status_code(response3, 200)

        #get
        response4 = MyRequests.get(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Field value has not changed")

    @allure.title("Creates new user and tries to edit its username without authorization")
    @pytest.mark.new_feature
    def test_user_edit_not_auth(self):
        # Register User
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_value_by_key(response1, "id")

        email = register_data["email"]
        firstName = register_data["firstName"]
        lastName = register_data["lastName"]
        password = register_data["password"]
        username = register_data["username"]

        user_id = self.get_json_value(response1, "id")

        # edit

        new_user_name = "unauthorized user"
        response2 = MyRequests.put(f"/user/{user_id}",
                                 data={"username": new_user_name})

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_response_content(response2, "Auth token not supplied")

    @allure.title("Creates and authorizes with new user, then creates another user and tries to edit its username")
    @pytest.mark.new_feature
    def test_user_edit_auth_with_another_user(self):
        # Register User
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_value_by_key(response1, "id")

        email = register_data["email"]
        firstName = register_data["firstName"]
        lastName = register_data["lastName"]
        password = register_data["password"]
        username = register_data["username"]

        user_id1 = self.get_json_value(response1, "id")

        # Login
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #register another user
        register_data = self.prepare_registration_data()
        response3 = MyRequests.post("/user/", data=register_data)
        user_id2 = self.get_json_value(response3, "id")

        # edit

        new_username = "unauthorised user"
        response4 = MyRequests.put(f"/user/{user_id2}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"username": new_username})

        Assertions.assert_status_code(response3, 200)

        # get
        response5 = MyRequests.get(f"/user/{user_id2}")

        Assertions.assert_json_value_by_name(response5, "username", username, "Field value has changed by unauthorized user")


    @allure.title("This test tries to change authorized user's email to invalid email w/o @")
    @pytest.mark.new_feature
    def test_user_edit_with_wrong_email(self):
        authorization_data = self.create_user_and_auth()
        user_id = authorization_data["user_id"]
        auth_sid = authorization_data["auth_sid"]
        token = authorization_data["x-csrf-token"]
        wrong_email = authorization_data["email"].replace("@", "")

        response = MyRequests.put(f"/user/{user_id}",
                                headers={"x-csrf-token": token},
                                cookies={"auth_sid": auth_sid},
                                data={"email": wrong_email})

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "Invalid email format")

        response2 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}, )
        initial_email = authorization_data["email"]
        Assertions.assert_json_value_by_name(response2, "email", initial_email,
                                             "Field value has changed to invalid")

    @allure.title("This test tries to change authorized user's first name to 'x'")
    @pytest.mark.skip
    def test_user_edit_short_first_name(self):
        authorization_data = self.create_user_and_auth()
        user_id = authorization_data["user_id"]
        auth_sid = authorization_data["auth_sid"]
        token = authorization_data["x-csrf-token"]
        short_first_name = "x"
        response1 = MyRequests.put(f"/user/{user_id}",
                                headers={"x-csrf-token": token},
                                cookies={"auth_sid": auth_sid},
                                data={"firstName": short_first_name})

        Assertions.assert_status_code(response1, 400)
        Assertions.assert_response_content(response1, '{"error":"Too short value for field firstName"}')

        response2 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                cookies={"auth_sid": auth_sid},)
        first_name = authorization_data["firstName"]
        Assertions.assert_json_value_by_name(response2, "firstName", first_name,
                                             "Field value has changed to invalid")