def user_input():
    while not (input_res := input('Введите число: ')).isdigit() or not \
            10 <= int(input_res) <= 20:
        print('Ошибка! Вы ввели не число или число не в диапазоне!')
    print('Работаем с числом', input_res)


user_input()