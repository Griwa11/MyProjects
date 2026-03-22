def my_func():
    words = []
    while new_word := (input('Введите любое слово: ')).lower():
        if new_word in words:
            print('Пароль ' + new_word
                  + ' уже присутствует в списке на позиции '
                  + str(words.index(new_word)))
            continue
        words.append(new_word)
    else:
        print(words)
    return words


def file_func(file_name, file_method):
    with open(file_name, file_method, encoding='utf-8') as file:
        for i in password_converting(res_words):
            file.write(str(i) + '\n')


def password_converting(target_words):
    res_list = []
    for word in target_words:
        res_list.append(word)
        res_list.append(word.upper())
        res_list.append(word.lower())
        res_list.append(word.title())
        res_list.append(''.join([word[ind].upper() if ind % 2 == 0 else
                                 word[ind] for ind in range(len(word))]))
        res_list.append(word[::-1])
        res_list.append(word + '1')
        res_list.append('1' + word)
        res_list.append(word.center(len(word) + 2, '-'))
        res_list.append(word + '_')
        res_list.append(word + '!')
        res_list.append('23' + word + '23')

    return res_list


if __name__ == '__main__':
    try:
        res_words = my_func()
    except KeyboardInterrupt:
        file_func('password.txt', 'w')
        print('\nВыход из программы!')