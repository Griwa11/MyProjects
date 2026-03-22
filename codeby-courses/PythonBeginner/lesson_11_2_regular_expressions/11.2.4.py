import re

with open('base-2.txt', encoding='utf-8') as file:
    search = re.compile(r'(\S+)@(\S+\.\w{2,3}):(.*)')
    res = re.findall(search, file.read())
    login_res = []
    domen_res = []
    password_res = []
    for i in range(len(res)):
        login_res.append(res[i][0])
        domen_res.append(res[i][1])
        password_res.append(res[i][2])
    login_res = set(login_res)
    domen_res = set(domen_res)
    password_res = set(password_res)

with open('login', 'w', encoding='utf-8') as file:
    for i in login_res:
        file.write(i + '\n')

with open('domen', 'w', encoding='utf-8') as file:
    for i in domen_res:
        file.write(i + '\n')

with open('passwords', 'w', encoding='utf-8') as file:
    for i in password_res:
        file.write(i + '\n')

print('Логинов:', len(login_res))
print('Доменов:', len(domen_res))
print('Паролей:', len(password_res))