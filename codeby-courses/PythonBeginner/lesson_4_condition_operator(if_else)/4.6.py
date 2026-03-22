months = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
          'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')


if ((user_input := int(input('Введите номер месяца от 1 до 12: ')))
        not in range(1, 13)):
    print('Номер месяца должен быть 1 до 12')

else:
    if 3 <= user_input <= 5:
        print('Весна', end=' ')
    elif 6 <= user_input <= 8:
        print('Лето', end=' ')
    elif 9 <= user_input <= 11:
        print('Осень', end=' ')
    else:
        print('Зима', end=' ')
    print(months[user_input - 1])