from colorama import Fore
import re


password = input('Введите пароль: ')
res = re.findall(r'[A-Z](?=.*?[_])(?=.*?[\d])(?=.*?[A-z])'
                 r'[a-zA-Z0-9_]{7,19}[a-z0-9]', password)


if password == ''.join(res):
    print(password, res, sep='\n')
    print(Fore.LIGHTGREEN_EX + ' Пароль принят!')
else:
    print(password, res, sep='\n')
    print(Fore.LIGHTRED_EX + ' Пароль не соответствует требованиям!')