# Sprint_7
test_courier_creation:

ошибка в test_create_courier_with_duplicate_login:
ожидалось: ответ - "Этот логин уже используется."
фактический результат: ответ - 'Этот логин уже используется. Попробуйте другой.'

ошибка в test_create_courier_without_required_fields:
можно создать курьера без обязательнх полей


есть тесты помеченные как @pytest.mark.xfail(reason="500 Error")
