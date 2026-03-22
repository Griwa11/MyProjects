def user_input(i):
    return i


def len_count():
    print('Символов в предложении: ', len(input_res))


def word_count():
    print('Слова в предложении: ', len(input_res.split()))


def sym_count():
    print('Сколько раз встречается каждый знак: ')
    for i in sorted(set(input_res)):
        print(i, '-', input_res.count(i))


if __name__ == '__main__':
    input_res = user_input(input('Введите предложение: '))
    len_count()
    word_count()
    sym_count()