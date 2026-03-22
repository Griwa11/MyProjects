reversed_list = [word[::-1] for word in input('Введите строку: ').split()]
print(' '.join(reversed_list))

[print(word[::-1], end=" ") for word in input("Введите строку: ").split()]
