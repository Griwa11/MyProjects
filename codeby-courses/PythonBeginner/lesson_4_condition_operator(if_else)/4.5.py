time_input_h = int(input('Введите часы: '))
time_input_m = int(input('Введите минуты: '))
time_input_s = int(input('Введите секунды: '))


if time_input_h > 23 or time_input_h < 0 or time_input_m > 60 or \
        time_input_m < 0 or time_input_s > 59 or time_input_s < 0:
    print('Введите числа от 0 до 23 для часов, от 0 до 60 для минут и '
          'от 0 до 59 для секунд')

else:
    time_output_1 = '0'*(2-len(str(time_input_h))) + str(time_input_h)
    time_output_2 = '0'*(2-len(str(time_input_m))) + str(time_input_m)
    time_output_3 = '0'*(2-len(str(time_input_s))) + str(time_input_s)
    print(time_output_1, time_output_2, time_output_3, sep=':')


hours = int(input('Введите часы: '))
minutes = int(input('Введите минуты: '))
seconds = int(input('Введите секунды: '))

if not (0 <= hours <= 23) or not (0 <= minutes <= 59) or not (0 <= seconds <= 59):
    print('Введите числа для часов от 0 до 23, и для минут и секунд от 0 до 59')
else:
    if hours < 10:
        hours = '0' + str(hours)
    if minutes < 10:
        minutes = '0' + str(minutes)
    if seconds < 10:
        seconds = '0' + str(seconds)
    print(hours, ':', minutes, ':', seconds)