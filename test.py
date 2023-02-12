import pytest
from main import calculate_delivery


@pytest.mark.parametrize(
    "distance, expected_result",
    [
        (-1, None),  # Отрицательное расстояние
        (0, None),  # Нет расстояния
        (1, 550),  # Среднее между 0 и 2
        (2, 550),  # Граничное 2
        (5, 600),  # Среднее между 2 и 10
        (10, 600),  # Граничное 10
        (15, 700),  # Среднее между 10 и 30
        (30, 700),  # Граничное 30
        (31, 800),  # Сверх 30
        (30000, None),  # Больше половины окружности планеты :)
    ]
)
def test_distance(distance, expected_result):
    """Тестируем функционал расчета расстояния"""
    result = calculate_delivery(distance=distance)
    assert expected_result == result, f'Неверное вычисление ({result}) при значении расстояния {distance}'


@pytest.mark.parametrize(
    "fragile_status, distance, expected_result",
    [
        (False, 1, 550),  # Не хрупкий груз
        (True, 1, 850),  # Хрупкий груз
        (True, 31, None),  # Хрупкий груз на расстояние более 30 км
    ]
)
def test_fragile(fragile_status, distance, expected_result):
    """Тестируем функционал хрупкости груза с учетом расстояния"""
    result = calculate_delivery(distance=distance, is_fragile=fragile_status)
    assert expected_result == result, f'Неверное вычисление ({result}) ' \
                                      f'при значении расстояния {distance} и хрупкости {fragile_status}'


@pytest.mark.parametrize(
    "oversized_status, expected_result",
    [
        (False, 550),  # НЕ габаритный груз
        (True, 650),  # Габаритный груз
    ]
)
def test_oversized(oversized_status, expected_result):
    """Тестируем функционал учета габаритов груза"""
    result = calculate_delivery(distance=1, is_oversized=oversized_status)
    assert expected_result == result, f'Неверное вычисление ({result}) при значении хрупкости {oversized_status}'


@pytest.mark.parametrize(
    "service_load, expected_result",
    [
        ('very high load', 880),  # Очень высока загруженность
        ('high load', 770),  # Просто высокая
        ('increase load', 660),  # Повышенная загруженность
        ('just load', 550),  # Никакой загруженности
    ]
)
def test_service_load(service_load, expected_result):
    """Тестируем функционал загруженности сервиса"""
    result = calculate_delivery(distance=1, service_load=service_load)
    assert expected_result == result, f'Неверное вычисление ({result}) при значении загруженности {service_load}'


@pytest.mark.parametrize(
    "price, expected_result",
    [
        (400, 550),  # Стоимость доставки 400
        (0, 150),  # Минимальная цена 0, стоимость складывается из условий
        (-1, None),  # Отрицательная стоимость
    ]
)
def test_price(price, expected_result):
    """Тестируем функционал минимальной стоимости, который не просили делать"""
    result = calculate_delivery(distance=1, price=price)
    assert expected_result == result, f'Неверное вычисление ({result}) при значении цены {price}'


@pytest.mark.parametrize(
    "distance, fragile_status, oversized_status, service_load, price, expected_result",
    [
        (15, True, True, 'high', 500, 1680),  # Все опции указаны явно
        (15, False, False, '', 400, 700),  # Все опции указанные по умолчанию (исключение distance)
    ]
)
def test_full_options(
        distance,
        fragile_status,
        oversized_status,
        service_load,
        price,
        expected_result
):
    """Тестируем функционал использования всех опций для расчета"""
    result = calculate_delivery(
        distance=distance,
        is_fragile=fragile_status,
        is_oversized=oversized_status,
        service_load=service_load,
        price=price
    )
    assert expected_result == result, f'Неверное вычисление ({result})'
