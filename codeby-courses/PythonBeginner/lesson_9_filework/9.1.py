num_list = []
for i in range(1, 10001):
    num_list.append(str(i) + '\n')
with open('numbers2.txt', 'w') as file:
    file.writelines(num_list)