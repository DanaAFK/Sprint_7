import pytest
import requests
import random
import string
from data import Data
import allure


@allure.title('Фикстура для генерации случайных строк')
@pytest.fixture
def generate_random_string():
    def _generate_random_string(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
    return _generate_random_string


@allure.title('Фикстура для регистрации нового курьера')
@pytest.fixture
def register_new_courier(generate_random_string):
    def _register_new_courier(login=None, password=None, first_name=None):
        if not login:
            login = generate_random_string()
        if not password:
            password = generate_random_string()
        if not first_name:
            first_name = generate_random_string()

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return requests.post(Data.CREATION_COURIER_URL, json=payload)
    return _register_new_courier


@allure.title('Фикстура для логина курьера')
@pytest.fixture
def login_courier():
    def _login_courier(login=None, password=None):
        payload = {
                "login": login,
                "password": password
            }
        return requests.post(Data.LOGIN_COURIER_URL, json=payload)
    return _login_courier


@allure.title('Фикстура для создания заказа')
@pytest.fixture
def creation_order():
    def _create_order(first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment, color):
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "address": address,
            "metroStation": metro_station,
            "phone": phone,
            "rentTime": rent_time,
            "deliveryDate": delivery_date,
            "comment": comment,
            "color": color
        }
        response = requests.post(Data.CREATION_ORDER_URL, json=payload)
        return response
    return _create_order


@allure.title('Фикстура для удаления курьера')
@pytest.fixture
def delete_courier():
    def _delete_courier(id=None):
        response = requests.delete(f"{Data.DELETE_COURIER}{id}")
        return response
    return _delete_courier


@pytest.fixture
def accept_order():
    def _accept_order(order_id=None, courier_id=None):
        url = f"{Data.ACCEPT_ORDER_URL}{order_id}"
        params = {"courierId": courier_id}
        response = requests.put(url, params=params)
        return response

    return _accept_order


@pytest.fixture
def get_order_by_number():
    def _get_order_by_number(track=None):
        url = f"{Data.GET_ORDER_BY_NUMBER}"
        params = {"t": track}
        response = requests.get(url, params=params)
        return response

    return _get_order_by_number