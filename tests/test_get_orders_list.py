import allure
import requests
from data import Data


class TestListOrders:
    @allure.title('Проверяем, что в тело ответа возвращается список заказов')
    def test_get_orders_list(self):
        response = requests.get(Data.GET_LIST_ORDER)
        assert response.status_code == 200
        assert isinstance(response.json().get("orders"), list)