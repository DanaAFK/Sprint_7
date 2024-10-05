import pytest
import allure


class TestGetOrderByNumber:
    @allure.title('Успешный поиск заказа по номеру')
    def test_get_order_by_number_success(self, creation_order, get_order_by_number):
        create_order = creation_order(
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
        track_order = create_order.json().get("track")
        assert track_order is not None

        get_order_by_number_response = get_order_by_number(track=track_order)
        assert get_order_by_number_response.status_code == 200
        assert isinstance(get_order_by_number_response.json().get("order"), dict)

    @allure.title('Запрос без номера заказа возвращает ошибку')
    def test_get_order_by_number_no_number(self, get_order_by_number):

        get_order_by_number_response = get_order_by_number(track=None)
        assert get_order_by_number_response.status_code == 400
        assert get_order_by_number_response.json().get("message") == "Недостаточно данных для поиска"

    @allure.title('Запрос с несуществующим заказом возвращает ошибку')
    def test_get_order_by_number_invalid_track(self,get_order_by_number):
        get_order_by_number_response = get_order_by_number(track="9292")
        assert get_order_by_number_response.status_code == 404
        assert get_order_by_number_response.json().get("message") == "Заказ не найден"
