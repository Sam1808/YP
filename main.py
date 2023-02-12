import argparse
from typing import Union


def calculate_delivery(
        distance: float,
        price: float = 400.0,
        service_load: str = '',
        is_oversized: bool = False,
        is_fragile: bool = False,
) -> Union[float, None]:
    """Функция рассчитывает стоимость доставки исходя из:
    {distance} - расстояния до пункта выдачи;
    {service_load} загруженность службы доставки (very high, high, increase);
    {is_oversized} габариты, где True большие, а False маленькие (по умолчанию);
    {is_fragile} хрупкость, True хрупкий, по умолчанию False;
    {price} минимальная стоимость доставки (по умолчанию уже 400).
    """

    if is_fragile and distance > 30 or distance <= 0 or distance >= 20038 or price < 0:  # По условию задачи (почти)
        return None

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

    if 'very' in service_load and 'high' in service_load:
        price *= 1.6
    elif 'high' in service_load:
        price *= 1.4
    elif 'increase' in service_load:
        price *= 1.2

    return price


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Please fill options for delivery')
    parser.add_argument('-d', '--delivery', type=float, required=True, help='Specify the delivery distance')
    parser.add_argument('-p', '--price', type=float, default=400, help='Add minimal delivery price (default 400)')
    parser.add_argument(
        '-l', '--load', type=str, default='', help='Specify current service load (very high, high or increase)'
    )
    parser.add_argument(
        '-o', '--is_oversized', type=bool, default=False, help='Is cargo oversized (default False)'
    )
    parser.add_argument(
        '-f', '--is_fragile', type=bool, default=False, help='Is cargo fragile (default False)'
    )

    args = parser.parse_args()

    total_price = calculate_delivery(
        distance=args.delivery,
        price=args.price,
        service_load=args.load,
        is_oversized=args.is_oversized,
        is_fragile=args.is_fragile
    )
    print(total_price)
