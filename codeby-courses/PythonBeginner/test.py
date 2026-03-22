import os

prefix = '11.2.'
file_names = range(1, 5)

for file_name in file_names:
    with open(prefix + str(file_name) + '.py', 'w', encoding='utf-8') as f:
        pass

print(f'Создано {len(file_names)} файлов')
