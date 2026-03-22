history = 'История Python, одного из самых простых языков \
программирования, началась в 1989 году.'

# print(history.find('про'))
# print(history.rfind('про'))
# print(history.find('ст'))
# print(history.rfind('ст')) использовал для поиска индексов

print(history[32:37] + history[3:5], end=' ')
print(history[47:50] + history[35:37] + history[-29:-31:-1], end=' ')
print(history[32:35] + history[1:5], end=' ')

history = history[::-1]
print(history[-33:-36:-1] + history[-2:-6:-1])