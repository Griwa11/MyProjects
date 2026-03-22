def shooting_time(x):
    shots_per_m = 1200
    mag_size = 250
    reload_time = 20
    shots_per_s = shots_per_m / 60
    if not 250 <= x <= 10000:
        print('Введите число от 250 до 10000.')
    else:
        time = x / shots_per_s
        reload_quantity = x // mag_size
        if x % mag_size == 0:
            reload_quantity -= 1
        time_w_reload = time + (reload_time*reload_quantity)
        print('Патроны закончатся через', time_w_reload, 'сек.')


shooting_time(int(input('Введите количество патронов: ')))


def ammo_off_time(ammo_count):
    if ammo_count not in range(250, 10001):
        print('Введите число от 250 до 10000.')
        return False

    fire_seconds = ((ammo_count - 1) // 250) * 20 + ammo_count / 20
    print('Патроны закончатся через', fire_seconds, 'сек.')


ammo_off_time(int(input('Введите количество патронов: ')))