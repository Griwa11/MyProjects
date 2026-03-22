import calendar
from colorama import Fore


def write_calendar(file_name):
    c = calendar.LocaleTextCalendar(locale="ru_RU.utf8")
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(c.formatyear(2023) + '\n')


def show_formatted(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        for num, line in enumerate(file.readlines(), 1):
            if num == 1 or "я" in line:
                print(f'{Fore.GREEN} {line} {Fore.RESET}', end='')
            else:
                print(line.replace('Сб Вс',
                                   f"{Fore.RED}Сб Вс{Fore.RESET}"), end='')


if __name__ == '__main__':
    target_name = 'calendar.txt'
    write_calendar(target_name)
    show_formatted(target_name)