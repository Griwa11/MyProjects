jewels = ('золото', 'алмазы', 'серебро', 'сапфиры', 'бронза',
'рубины', 'платина', 'изумруды', 'палладий', 'аметисты')

for i in range(2):
    for num, gem in enumerate(jewels[i::2], 1):
        print(num, gem)