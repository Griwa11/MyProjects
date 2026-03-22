import re

text = '''Примеры расширений файлов:
wald.jpeg
wow.mp4
book.txt
forest.png
fox.tiff
wood.pdf
hub.gif
small.zip
sound.mp3
'''

res = re.findall(r'\w+\.(?:jpeg|png|tiff|gif)$', text, re.M)
for i in res:
    print(i)