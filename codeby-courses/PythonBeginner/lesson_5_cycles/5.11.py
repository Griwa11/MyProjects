user_input = input('Введите любое число от 0 до 30: ')

for i in range(0, 20, 2):
    if i == int(user_input):
        print('Аварийно завершили цикл.')
        break
    print(i)
else:
    print('Число пользователя =', user_input, '\nПри переборе не попалось!')

print('\nВышли из цикла!')