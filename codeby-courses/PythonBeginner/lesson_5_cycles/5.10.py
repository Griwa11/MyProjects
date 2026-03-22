target_ints = (1, 3, 3, 4, 7, 9)

result_list = []
for i in target_ints:
    if target_ints.count(i) > 1:
        result_list.append(i)

print(result_list)

target_ints = (1, 3, 3, 4, 7, 9)

result_list = list(target_ints)
for i in target_ints:
    if target_ints.count(i) == 1:
        result_list.remove(i)

print(result_list)