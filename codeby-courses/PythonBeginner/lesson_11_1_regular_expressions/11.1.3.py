import re

with open('job.txt', encoding='utf-8') as file:
    print('\n'.join(re.findall(r'[К-С].{5}к', file.read())))