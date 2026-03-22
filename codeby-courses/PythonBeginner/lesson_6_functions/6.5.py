def my_func(word='python'):
    words = []
    words.append(word)
    while new_word := input('Введите любое слово: '):
        if new_word in words:
            print('Строка ' + new_word
                  + ' уже присутствует в списке на позиции '
                  + str(words.index(new_word)))
            break
        words.append(new_word)
    else:
        print(words)


my_func()