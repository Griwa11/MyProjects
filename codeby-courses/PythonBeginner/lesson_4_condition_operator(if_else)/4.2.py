user_input = int(input('Введите возраст: '))

if not 1 <= user_input <= 100:
    print('Введите число от 1 до 100')
else:
    if 1 <= user_input <= 6:
        print('Детство это - прекрасно!')
    elif 7 <= user_input <= 17:
        print('Учиться, учиться, учиться...')
    elif 18 <= user_input <= 64:
        print('Теперь ты можешь делать всё что угодно!')
    else:
        print('Заслуженный отдых')