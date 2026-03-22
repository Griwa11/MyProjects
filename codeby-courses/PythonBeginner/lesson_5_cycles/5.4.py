names = ('Ваня', 'Даня', 'Саня')
actions = ('учит', 'знает', 'выбирает')
languages = ('Python', 'PHP', 'C#')

for name in names:
    for action in actions:
        for language in languages:
            print(name, action, language)