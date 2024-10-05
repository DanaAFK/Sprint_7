import pytest
import allure


class TestCreateOrder:
    @allure.title("Тест создания заказа c различными опциями цвета")
    @allure.description("Создаем заказ с параметризованным цветом. Проверяем, что заказ был успешно создан. Проверяем, что в ответе есть поле track")
    @pytest.mark.parametrize(
        "color, description",
        [
            (["BLACK"], "только черный цвет"),
            (["GREY"], "только серый цвет"),
            (["BLACK", "GREY"], "оба цвета"),
            ([], "без цвета"),
        ]
    )
    def test_create_order_with_color(self, creation_order, color, description):
        first_name = "Naruto"
        last_name = "Uchiha"
        address = "Konoha, 142 apt."
        metro_station = 4
        phone = "+7 800 355 35 35"
        rent_time = 5
        delivery_date = "2020-06-06"
        comment = "Saske, come back to Konoha"

        response = creation_order(
            first_name=first_name,
            last_name=last_name,
            address=address,
            metro_station=metro_station,
            phone=phone,
            rent_time=rent_time,
            delivery_date=delivery_date,
            comment=comment,
            color=color
        )

        assert response.status_code == 201
        response_data = response.json()
        assert "track" in response_data
