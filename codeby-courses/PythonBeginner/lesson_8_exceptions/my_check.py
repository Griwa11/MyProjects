def get_user_input(user_input, type_input=int):
    try:
        input_res = input(user_input)
        result = type_input(input_res)
    except ValueError:
        print('Ошибка ввода!\nВвод пользователя должен был содержать '
              '<class "int">')
    else:
        return result