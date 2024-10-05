import pytest
import requests
import allure
from data import Data


class TestCourierDelete:
    @allure.title('Тест успешного удаления курьера')
    def test_delete_courier(self, register_new_courier, generate_random_string, login_courier, delete_courier):
        login = generate_random_string()
        password = "password123"
        first_name = "CourierTest"

        register_new_courier(login=login, password=password, first_name=first_name)

        login_response = login_courier(login=login, password=password)
        assert login_response.status_code == 200

        login_data = login_response.json()
        courier_id = login_data["id"]

        response = delete_courier(id=courier_id)
        assert response.status_code == 200
        assert response.json().get("ok") is True

    @pytest.mark.xfail(reason="500 Error")
    @allure.title('Тест удаления курьера без id')
    def test_delete_courier_no_id(self):
        response = requests.delete(f"{Data.DELETE_COURIER}:id")
        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для удаления курьера"

    @allure.title('Тест удаления курьера c несуществующим id')
    def test_delete_courier_nonexistent_id(self, delete_courier):
        response = delete_courier(id='09662')
        assert response.status_code == 404
        assert response.json().get("message") == "Курьера с таким id нет."

