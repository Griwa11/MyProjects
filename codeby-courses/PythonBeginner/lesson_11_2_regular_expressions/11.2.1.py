import re

text = 'Сначала был адрес http://yandex.ru, потом стал https://yandex.ru. \
Гугл https://google.com имеет шире охват чем https://yandex.ru.'

res = set(re.findall(r'https?\S{3}[a-z]+\.\w{2,3}', text))

for i in res:
    print(i)


res = set(re.findall(r'https?://[a-z0-9]+\.\w{2,3}', text))

for i in res:
    print(i)

res = re.findall(r'(https?://\w+\.\w{2,3})(?!.*\1)', text)
print('\n'.join(res))
