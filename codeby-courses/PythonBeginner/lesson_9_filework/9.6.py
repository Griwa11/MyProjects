with open('surnames.txt', 'r', encoding='utf-8') as file:
    data_list = [i.replace('\n', '') for i in file.readlines()]
    for surname in data_list:
        if surname.endswith(('ВА', 'НА', 'АЯ')):
            with open('women.txt', 'a', encoding='utf-8') as file_w:
                file_w.write(surname.title() + '\n')
        else:
            with open('men.txt', 'a', encoding='utf-8') as file_m:
                file_m.write(surname.title() + '\n')