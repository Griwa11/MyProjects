import time
from colorama import Fore
import lorem_text.lorem as lt
import random


def countdown():
    for s in range(3, 0, -1):
        print(s, end="... ", flush=True)
        time.sleep(1)
    print(Fore.RED, 'Начали!\n', Fore.RESET)
    time.sleep(1)


def generate_str():
    text = lt.words(random.randint(5, 15))
    return text


def input_time_results(target_string):
    time_start = time.time()
    input_res = input(' ' + Fore.LIGHTCYAN_EX + target_string + Fore.RESET
                      + '\nВведите текст выше: ')
    time_end = time.time() - time_start
    return input_res, time_end


def main_start():
    countdown()
    target_text = generate_str()
    input_res, time_res = input_time_results(target_text)
    if target_text == input_res:
        output(input_res, time_res)
    else:
        print(Fore.LIGHTYELLOW_EX + ' Увы в тексте вы допустили ошибки'
              + Fore.RESET, end='')
        try_again()


def output(input_res, time_res):
    filler = '#' * 36
    print_speed = len(input_res) / time_res * 60
    print(Fore.LIGHTGREEN_EX + filler)
    print(' Вы отлично справились! '.center(len(filler), '#'))
    print((' Время печати: ' + str(round(time_res, 2)) + ' с. ')
          .center(len(filler), '#'))
    print((' Скорость печати: ' + str(round(print_speed, 2)) + ' зн/м ')
          .center(len(filler), '#'))
    print(filler + Fore.RESET)
    try_again()


def try_again():
    while input('\nНачать заново(д) или завершить программу(н)? ') == 'д':
        main_start()
    else:
        print('До новых встреч!')


if __name__ == '__main__':
    main_start()