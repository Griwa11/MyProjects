from my_check import get_user_input
import random


def counting(num_1, num_2):
    while not 1 <= num_1 <= 10:
        num_1 = get_user_input('Введите число от 1 до 10: ')
    if num_1 == num_2:
        return num_1 + num_2
    return sum(range(num_1, num_2 + 1))


print(counting(get_user_input('Введите число от 1 до 10: '),
               random.randint(2, 2)))