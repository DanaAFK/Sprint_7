import pytest
import allure


class TestCourierCreation:
    @allure.title('Тест успешного создания курьера')
    def test_create_courier_successfully(self, register_new_courier):
        response = register_new_courier()
        assert response.status_code == 201
        assert response.json().get("ok") is True

    @allure.title('Тест создания курьера с повторяющимся логином')
    @allure.description('Создаем курьера с уникальным логином: Первое создание должно быть успешным.Пытаемся создать курьера с тем же логином:Повторное создание должно вернуть код 409')
    def test_create_courier_with_duplicate_login(self, register_new_courier, generate_random_string):
        login = generate_random_string()
        response = register_new_courier(login=login)
        assert response.status_code == 201

        response_duplicate = register_new_courier(login=login)
        assert response_duplicate.status_code == 409
        assert response_duplicate.json().get("message") == "Этот логин уже используется"

    @allure.title('Тест создания курьера без обязательных полей')
    @allure.description('Тест проверяет, что отсутствие одного из обязательных полей возвращает ошибку 400')
    @pytest.mark.parametrize(
        "password, first_name, missing_field",
        [
            ("password1", "Dana", "логин"),
            (None, "Dana", "пароль"),
            ("password3", None, "имя"),
        ]
    )
    def test_create_courier_without_required_fields(self, register_new_courier, generate_random_string, password,
                                                    first_name, missing_field):
        login = generate_random_string()

        response = register_new_courier(login=login, password=password, first_name=first_name)
        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для создания учетной записи"