hours, minutes = input('Введите время: ').split(':')
total_minutes = 60 * int(hours) + int(minutes)

if total_minutes < 360 or total_minutes > 1080:
    print('Солнце за горизонтом!')
else:
    minutes_after_sunrise = total_minutes - 360
    degrees = minutes_after_sunrise * 180 / 720
    print('Угол солнца:', degrees, 'градусов')