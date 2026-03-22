def user_input():
    exchange_rate = float(input('Введите курс доллара к рублю: '))
    quantity = float(input('Ввдетие количество долларов: '))
    exchange_result(exchange_rate, quantity)


def exchange_result(rate, qnt):
    print(f'По курсу {rate:.2f} рублей за доллар вы получите '
          f'{(rate * qnt):.2f} рублей')
    print('По курсу %.2f рублей за доллар вы получите %.2f рублей'
          % (rate, rate*qnt))
    res = ('По курсу {:.2f} рублей за доллар вы получите {:.2f} рублей'.format
           (rate, rate*qnt))
    print(res)


if __name__ == '__main__':
    user_input()