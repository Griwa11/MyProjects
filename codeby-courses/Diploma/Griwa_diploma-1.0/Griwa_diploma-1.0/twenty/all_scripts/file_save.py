def save(name, art, color=False):
    reset_color = r"\033[0m"
    if color is False:
        formatted_data = f"print(r'''\n{art}''')"
    else:
        formatted_data = f"print({color} + r'''\n{art}''' + {reset_color})"
    with open(name + '.txt', 'a', encoding='utf-8') as file:
        file.write(formatted_data + '\n')