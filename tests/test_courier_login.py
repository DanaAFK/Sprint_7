import pytest
import allure


@allure.title("Тест логина курьера")
@allure.feature("Логин курьера")
class TestCourierLogin:

    @allure.title("Курьер может авторизоваться")
    @allure.description("Проверка успешного логина при передаче правильного логина и пароля.")
    def test_courier_can_login(self, register_new_courier, login_courier, generate_random_string):
        login = generate_random_string()
        password = "password123"
        first_name = "CourierTest"

        register_new_courier(login=login, password=password, first_name=first_name)

        response = login_courier(login=login, password=password)
        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.xfail(reason="500 Error")
    @allure.title("Ошибка при отсутствии логина или пароля")
    @pytest.mark.parametrize(
        "login, password, missing_field",
        [
            (None, "password123", "логин"),
            ("login", None, "пароль")
        ]
    )
    def test_login_missing_required_fields(self, login_courier, login, password, missing_field):
        response = login_courier(login=login, password=password)
        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для входа"

    @allure.title("Ошибка при неверных логине или пароле")
    def test_login_with_incorrect_credentials(self, register_new_courier, login_courier, generate_random_string):
        login = generate_random_string()
        password = "password1234"
        first_name = "CourierTest"

        register_new_courier(login=login, password=password, first_name=first_name)

        response = login_courier(login="wrong_login", password=password)
        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"

        response = login_courier(login=login, password="wrong_password")
        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"

    @allure.title("Ошибка при попытке авторизации под несуществующим пользователем")
    def test_login_nonexistent_user(self, login_courier):
        response = login_courier(login="nonexistent_login", password="password123")
        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"