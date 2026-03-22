targets = "7 раз отмерь, 1 раз отрежь.;Не имей 100 рублей, а \
имей 100 друзей.;1 за всех и все за 1."

targets_tuple = tuple(targets.split(';'))

for phrase in targets_tuple:
    num = 0
    for elem in phrase[-1].split():
        if elem.isnumeric():
            num += int(elem)
    print(phrase, num)