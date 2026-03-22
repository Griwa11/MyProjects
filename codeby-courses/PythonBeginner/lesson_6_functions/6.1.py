def count_sym(target_text):
    """
    Функция считает количество символов во входящей строке без учёта пробелов.
    """
    print('Количество символов в предложении: ',
          len(target_text.replace(' ', '')))


count_sym(input('Введите предложение: '))
print(count_sym.__doc__)