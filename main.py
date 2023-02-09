from typing import Union


def calculate_delivery(
        distance: float,
        price: float = 400.0,
        service_load: str = '',
        is_oversized: bool = False,
        is_fragile: bool = False,
) -> Union[float, str]:
    """Функция рассчитывает стоимость доставки исходя из:
    {distance} - расстояния до пункта выдачи;
    {service_load} загруженность службы доставки (very high, high, increase);
    {is_oversized} габариты, где True большие, а False маленькие (по умолчанию);
    {is_fragile} хрупкость, True хрупкий, по умолчанию False;
    {price} минимальная стоимость доставки (по умолчанию уже 400).
    """
    if is_fragile and distance > 30:
        return 'Forbidden. You are trying to ship fragile cargo over 30 kilometers !'

    if is_fragile:
        price += 300

    price = price + 200 if is_oversized else price + 100

    if distance > 30:
        price += 300
    elif 10 < distance <= 30:
        price += 200
    elif 2 < distance <= 10:
        price += 100
    elif 0 < distance <= 2:
        price += 50

    service_load = service_load.lower()

    if 'very' and 'high' in service_load:
        price *= 1.6
    elif 'high' in service_load:
        price *= 1.4
    elif 'increase' in service_load:
        price *= 1.2

    return format(price, '.2f')


if __name__ == '__main__':

    print(calculate_delivery(distance=31, service_load='increase day'))
