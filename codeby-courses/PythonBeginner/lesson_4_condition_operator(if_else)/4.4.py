user_input = len(input('Введите строку: '))
if user_input > 100:
    print('Количество символов не должно быть больше 100!')
else:
    if user_input != 11 and user_input % 10 == 1:
        print('В строке', user_input, 'символ')
    elif user_input % 10 in (2, 3, 4) and user_input not in (12, 13, 14):
        print('В строке', user_input, 'символа')
    else:
        print('В строке', user_input, 'символов')