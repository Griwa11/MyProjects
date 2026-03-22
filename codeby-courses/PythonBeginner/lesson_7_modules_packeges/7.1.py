import string
import random

str_list = string.ascii_letters + string.digits

print('Список случайных 10 символов:\n', random.sample(str_list, 10))
print('Список случайных 10 символов:\n', random.choices(str_list, k=10))
print('Список случайных 10 символов:\n', [random.choice(str_list)
                                          for _ in range(10)])
