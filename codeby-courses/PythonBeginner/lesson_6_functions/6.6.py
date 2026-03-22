def my_func(*args):
    args = [int(num) for num in args[0]]
    if len(args) == 1:
        calc = 3.14 * (args[0] / 2) ** 2
        print('Площадь круга:', str(round(calc, 2)), 'кв. м.')
    elif len(args) == 2:
        calc = args[0] * args[1]
        print('Площадь прямоугольника:', str(calc), 'кв. м.')
    elif len(args) == 3:
        triangle_side_size = (args[0] + args[1] + args[2]) / 3
        calc = ((3 ** 0.5) / 4) * (triangle_side_size ** 2)
        print('Площадь треугольника:', str(round(calc, 2)), 'кв. м.')


my_func(input('Введите аргументы: ').split())