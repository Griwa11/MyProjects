import animals
import random
from my_check import get_user_input


def menu():
    print('Help:\n')
    for picture_id in picture_nums:
        print('\t', str(picture_id) + ')', picture_nums.get(picture_id)[0])

    user_pic_choice = int(get_user_input('\nВведите номер рисунка: '))
    return user_pic_choice


def picture_print(menu_option):

    while not 1 <= menu_option <= 7:
        menu_option = int(get_user_input('\nВведите число от 1 до 7: '))
    if menu_option == 7:
        print(random.choice(picture_nums)[1])
    else:
        print(picture_nums.get(menu_option)[1])


if __name__ == '__main__':
    picture_nums = {1: ('deer', animals.deer), 2: ('cat', animals.cat),
                    3: ('cow', animals.cow), 4: ('frog', animals.frog),
                    5: ('bat', animals.bat),
                    6: ('butterfly', animals.butterfly),
                    7: ('random',)}

    picture_print(menu())