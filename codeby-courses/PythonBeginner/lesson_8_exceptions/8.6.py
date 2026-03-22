import random


def input_check():
    try:
        number = int(input('Введите число от 1 до 10: '))
    except (ValueError, EOFError):
        print("Ошибка! Вы ввели не число!")
    else:
        return number


def game():
    for i in range(3):
        if number := input_check():
            if number == random_number:
                print('Ты победил!')
                break
            elif i < 2:
                if not 1 <= number <= 10:
                    print('Ошибка! Введите число от 1 до 10')
                if number > random_number:
                    print('Ваше число больше')
                elif number < random_number:
                    print('Ваше число меньше')
    else:
        print('Удача не на твоей стороне, попробуй ещё!')


if __name__ == '__main__':
    random_number = random.randint(1, 10)
    game()