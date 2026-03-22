import requests
import sys
import os

DOMAIN = ""
DIRS = []


def greetings():
    """Функция отображает приветствие пользователя"""
    print('''
╔═══╗╔══╗╔═══╗     ╔═══╗╔╗─╔╗╔════╗╔════╗╔═══╗╔═══╗
╚╗╔╗║╚╣║╝║╔═╗║     ║╔══╝║║─║║╚══╗═║╚══╗═║║╔══╝║╔═╗║
─║║║║─║║─║╚═╝║     ║╚══╗║║─║║──╔╝╔╝──╔╝╔╝║╚══╗║╚═╝║
─║║║║─║║─║╔╗╔╝     ║╔══╝║║─║║─╔╝╔╝──╔╝╔╝─║╔══╝║╔╗╔╝
╔╝╚╝║╔╣║╗║║║╚╗     ║║───║╚═╝║╔╝═╚═╗╔╝═╚═╗║╚══╗║║║╚╗
╚═══╝╚══╝╚╝╚═╝     ╚╝───╚═══╝╚════╝╚════╝╚═══╝╚╝╚═╝
          ''')


def check_wordlist_file(path_to_wordlist):
    """Функция проверяет наличие файла со словарём"""
    if not os.path.isfile(path_to_wordlist.replace("\'", "")):
        print(f"{path_to_wordlist}\nФайл со словарём не найден.")
        sys.exit(0)
    fill_dirs_from_file(path_to_wordlist)


def check_site_annotaion(hostname):
    """Функция проверяет есть ли коннект с хостом"""
    try:
        response = requests.get(hostname, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}, timeout=1)
        response.raise_for_status()
        if response.status_code == 200:
            print('OK!')
    except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
        print('ERROR: %s' % e)

    set_url_format(hostname)


def set_url_format(hostname):
    """Функция проверяет форматирование url сайта"""
    global DOMAIN
    if hostname[-1] != "/":
        hostname += "/"
    else:
        DOMAIN = hostname


def check_args_qnt(args_qnt):
    """Функция проверяет количество аргументов"""
    if len(args_qnt) != 3:
        print('To use the program, specify the domain and wordlist https://site.com /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt')
        sys.exit(0)


def check_app_keys():
    """Функция проверяет правильность аргументов"""
    # Количество аргументов
    check_args_qnt(sys.argv)
    # Доступность файла словаря
    check_wordlist_file(sys.argv[2])
    # Доступность хоста
    check_site_annotaion(sys.argv[1])
    print(f"\nРаботаем с сайтом {sys.argv[1]}. Путь к словарю {sys.argv[2]}\n")


def fill_dirs_from_file(dirs_file):
    """Функция читает файл с адресами папок в список"""
    with open(dirs_file, "r") as reader:
        for line in reader.readlines():
            DIRS.append(line)
    print("\nЗагружено строк из словаря: " + str(len(DIRS)) + "\n")


def get_site_dirs():
    """Функция проверки директорий"""
    counter = 0
    try:
        for target_dir in DIRS:
            target_url = DOMAIN + target_dir.strip() + "/"
            host_answer = requests.get(target_url)
            counter += 1
            if host_answer.status_code == 404:
                continue
            else:
                print(f"{counter} of {len(DIRS)}\t{host_answer.status_code}\t{target_url}")
    except KeyboardInterrupt:
        print('  ERROR: manually stop Ctrl+C')


if __name__ == "__main__":
    greetings()
    check_app_keys()
    get_site_dirs()
