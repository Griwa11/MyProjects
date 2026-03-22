from random import randint
from colorama import Fore


def toss():
    res = randint(1, 6) + randint(1, 6)
    return res


def score_count(p1_score, p2_score):
    p1_str = f'Игрок Дима набрал {p1_score:02d} очк.'
    p2_str = f'Игрок Вова набрал {p2_score:02d} очк.'
    return p1_str, p2_str


def game():
    while (p1_points := toss()) == (p2_points := toss()):
        print(f'{score_count(p1_points, p2_points)[0]}\n'
              f'{score_count(p1_points, p2_points)[1]}\n'
              f'Очки у обоих игроков совпали, перебрасываем кости')

    winner(p1_points, p2_points)


def winner(p1, p2):
    if p1 > p2:
        print(f'{Fore.GREEN}{score_count(p1, p2)[0]} You winner!{Fore.RESET}'
              f'\n{score_count(p1, p2)[1]}')
    else:
        print(f'{Fore.GREEN}{score_count(p1, p2)[1]} You winner!{Fore.RESET}'
              f'\n{score_count(p1, p2)[0]}')


if __name__ == '__main__':
    game()