import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    exclude_params = [
        ("no_password"),
        ("no_firstName"),
        ("no_lastName"),
        ("no_username"),
        ("no_email")
    ]


    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post('/user/', data=data)
        Assertions.assert_json_value_by_key(response, "id")
        Assertions.assert_status_code(response, 200)

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user/', data=data)
        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists"

    def test_create_user_with_incorrect_email(self):
        data = self.prepare_registration_data()
        data["email"] = data["email"].replace("@", "")
        response = MyRequests.post('/user/', data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, 'Invalid email format')

    @pytest.mark.parametrize("condition", exclude_params)
    def test_create_user_without_field(self, condition):
        expected_result = f"The following required params are missed: {condition[3:]}"
        if condition == "no_password":
            data = self.prepare_registration_data()
            del data["password"]
        if condition == "no_firstName":
            data = self.prepare_registration_data()
            del data["firstName"]
        if condition == "no_lastName":
            data = self.prepare_registration_data()
            del data["lastName"]

        if condition == "no_username":
            data = self.prepare_registration_data()
            del data["username"]

        if condition == "no_email":
            data = self.prepare_registration_data()
            del data["email"]


        response = MyRequests.post('/user/', data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, expected_result)


    def test_username_min_length(self):
        short_username = "n"
        data = self.prepare_registration_data()
        data["username"] = short_username
        response = MyRequests.post('/user/', data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "The value of 'username' field is too short")


    def test_username_max_length(self):


        username_max_length = 250
        long_username = self.generate_long_username(username_max_length)
        data = self.prepare_registration_data()
        data["username"] = long_username
        response = MyRequests.post('/user/', data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "The value of 'username' field is too long")