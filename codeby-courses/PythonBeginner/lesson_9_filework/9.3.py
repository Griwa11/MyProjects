import time
from colorama import Fore


def check_city():
    with open('city.txt', 'r', encoding='utf-8') as file:
        city_list = [i.replace('\n', '') for i in file]
        user_input = input('Введите первую и последнюю букву города: ')
        res_list = []
        for i in city_list:
            if i.lower()[0] + i[-1] == user_input:
                print(Fore.GREEN + i + Fore.RESET)
                res_list.append(i)

    print('Найдено городов:', len(res_list))
    if input('Записать данные в файл (д/н)? ') == 'д':
        save(res_list)
    return res_list


def save(city_res_list):
    file_name = 'results' + time.strftime('_%m-%d_%H-%M-%S')
    with open(file_name, 'w', encoding='utf-8') as file:
        for city in city_res_list:
            file.write(str(city) + '\n')
        print('Записали данные в файл', Fore.YELLOW + file_name + Fore.RESET)


if __name__ == '__main__':
    check_city()