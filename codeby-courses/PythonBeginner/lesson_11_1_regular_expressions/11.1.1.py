import re

text = 'Московское время 10:36:06'

print(''.join(re.findall(r'(?:\d{2}:?){3}', text)))