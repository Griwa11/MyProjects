import calendar as cal
from colorama import Fore


with open('calendar.txt', 'w', encoding='utf-8') as file:
    cal_print = file.write(cal.LocaleTextCalendar(locale='Russian_Russia')
                           .formatyear(2024))


with open('calendar.txt', 'r', encoding='utf-8') as file:
    for i in file:
        if 'а' in i.lower() or '2024' in i:
            print(Fore.GREEN + i.replace('\n', '') + Fore.RESET)
        elif 'Вс' in i:
            print(i.replace('Сб Вс', Fore.RED + 'Сб Вс' + Fore.RESET))
        else:
            print(i.replace('\n', ''))