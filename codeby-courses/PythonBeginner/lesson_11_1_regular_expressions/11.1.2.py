import re

with open('proxy.txt', encoding='utf-8') as file:
    print('\n'.join(re.findall(r'(?:\d{1,3}\.){3}\d{1,3}',
                               file.read())))