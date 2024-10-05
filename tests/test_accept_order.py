import pytest
import allure


@allure.title('Тесты на принятие заказа')
@allure.feature('Принятие заказа')
class TestAcceptOrder:

    @allure.title('Тест успешного принятия заказа')
    def test_accept_order_success(self, register_new_courier, generate_random_string, login_courier, creation_order, accept_order):
        login = generate_random_string()
        password = "password123"
        first_name = "CourierTest"

        register_response = register_new_courier(login=login, password=password, first_name=first_name)
        assert register_response.status_code == 201

        login_response = login_courier(login=login, password=password)
        assert login_response.status_code == 200

        courier_id = login_response.json().get("id")
        assert courier_id is not None

        order_response = creation_order(
            first_name="Test",
            last_name="User",
            address="Test address",
            metro_station=4,
            phone="+7 999 999 99 99",
            rent_time=5,
            delivery_date="2024-10-10",
            comment="Test order",
            color=[]
        )
        assert order_response.status_code == 201

        order_id = order_response.json().get("track")
        assert order_id is not None

        accept_response = accept_order(order_id=order_id, courier_id=courier_id)
        assert accept_response.status_code == 200
        assert accept_response.json().get("ok") is True

    @allure.title('Ошибка при отсутствии ID курьера')
    def test_accept_order_no_courier_id(self, creation_order, accept_order):
        order_response = creation_order(
            first_name="Test",
            last_name="User",
            address="Test address",
            metro_station=4,
            phone="+7 999 999 99 99",
            rent_time=5,
            delivery_date="2024-10-10",
            comment="Test order",
            color=[]
        )
        assert order_response.status_code == 201

        order_id = order_response.json().get("track")
        assert order_id is not None

        accept_response = accept_order(order_id=order_id, courier_id=None)
        assert accept_response.status_code == 400
        assert accept_response.json().get("message") == "Недостаточно данных для поиска"

    @allure.title('Ошибка при неверном ID курьера')
    def test_accept_order_invalid_courier_id(self, creation_order, accept_order):
        order_response = creation_order(
            first_name="Test",
            last_name="User",
            address="Test address",
            metro_station=4,
            phone="+7 999 999 99 99",
            rent_time=5,
            delivery_date="2024-10-10",
            comment="Test order",
            color=[]
        )
        assert order_response.status_code == 201

        order_id = order_response.json().get("track")
        assert order_id is not None
        invalid_courier_id = 999999
        accept_response = accept_order(order_id=order_id, courier_id=invalid_courier_id)
        assert accept_response.status_code == 404
        assert accept_response.json().get("message") == "Курьера с таким id не существует", "Ожидалось сообщение о несуществующем курьере"

    @pytest.mark.xfail(reason="500 Error")
    @allure.title('Ошибка при отсутствии ID заказа')
    def test_accept_order_no_order_id(self, register_new_courier, generate_random_string, login_courier, accept_order):
        login = generate_random_string()
        password = "password123"
        first_name = "CourierTest"

        register_response = register_new_courier(login=login, password=password, first_name=first_name)
        assert register_response.status_code == 201

        login_response = login_courier(login=login, password=password)
        assert login_response.status_code == 200

        courier_id = login_response.json().get("id")
        assert courier_id is not None

        accept_response = accept_order(order_id=None, courier_id=courier_id)
        assert accept_response.status_code == 400
        assert accept_response.json().get("message") == "Недостаточно данных для поиска"

    @allure.title('Ошибка при неверном ID заказа')
    def test_accept_order_invalid_order_id(self, register_new_courier, generate_random_string, login_courier, accept_order):
        login = generate_random_string()
        password = "password123"
        first_name = "CourierTest"

        register_response = register_new_courier(login=login, password=password, first_name=first_name)
        assert register_response.status_code == 201

        login_response = login_courier(login=login, password=password)
        assert login_response.status_code == 200

        courier_id = login_response.json().get("id")
        assert courier_id is not None

        invalid_order_id = 999999
        accept_response = accept_order(order_id=invalid_order_id, courier_id=courier_id)
        assert accept_response.status_code == 404
        assert accept_response.json().get("message") == "Заказа с таким id не существует"