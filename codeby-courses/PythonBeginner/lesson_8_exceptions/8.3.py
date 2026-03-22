def get_user_input(user_input, type_input=int):
    try:
        result = type_input(input(user_input))
    except ValueError:
        print('Ошибка ввода!\nВвод пользователя должен был содержать',
              str(type_input))
    else:
        return result


print(get_user_input('Ввод: '))