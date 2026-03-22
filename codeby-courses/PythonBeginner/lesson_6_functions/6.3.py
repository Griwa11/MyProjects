word = 'predator'
compare = lambda x: 'Это слово больше, чем ' + word if len(x) > len(word)\
    else 'Это слово меньше, чем ' + word

print(compare(input('Введите слово: ')))