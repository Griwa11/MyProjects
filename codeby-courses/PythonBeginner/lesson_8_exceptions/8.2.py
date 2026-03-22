def user_input_division(input_1, input_2):
    try:
        func_res = int(input_1)/int(input_2)
    except ZeroDivisionError:
        print('На ноль делить нельзя!')
    except ValueError:
        print('Возникла какая-то ошибка!')
    else:
        return func_res


if __name__ == '__main__':
    var_1, var_2 = [input('Введите число: ') for _ in range(2)]
    if (result := user_input_division(var_1, var_2)) is None:
        print('Программа остановлена! Поделить', var_1, 'на', var_2,
              'нельзя!')
    else:
        print('Результат деления равен', result)