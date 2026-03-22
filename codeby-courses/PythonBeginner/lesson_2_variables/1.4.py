man_time_part = 2
man_vel_kmh = 4
car_vel_ms = 30
car_time_full = 10

car_vel_kmh = (car_vel_ms * 60 * 60) / 1000
distance_km = (car_vel_kmh * car_time_full) / 60

man_dis_left = distance_km - (man_vel_kmh * man_time_part)
man_time_left = man_dis_left / man_vel_kmh

print('Пешеходу осталось идти', man_time_left, 'часа')