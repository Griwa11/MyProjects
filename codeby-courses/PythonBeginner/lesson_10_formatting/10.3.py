with open('symbol.txt', 'r') as reader:
    while first_8 := reader.read(8):
        print(f'{first_8[:4]:,>12}{first_8[4:]:.<12}')