list_1 = [val for val in range(2, 51, 4)]
print(list_1)
list_2 = [val for val in range(100, 66, -3)]
print(list_2)

languages = 'Python Golang PHP C# Java'
dict_1 = {elem: elem[0] for elem in languages.split()}
print(dict_1)