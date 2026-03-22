from all_scripts.design import Decor as Dec
from all_scripts.all_items import all_styles
from all_scripts.file_save import save


def print_menu():
    """Prints the menu of all fonts.
    Also includes - All Items(print all fonts) and Exit options.
    Collects data from options dict."""
    for index, option_name in options.items():
        print(f"{str(index):>3}. {option_name[0]:<15}",
              end=' ' if index % 2 == 1 else '\n')


def font_choice():
    """User selects font of his choice from the printed menu.
    If user inputs the wrong choice(any number outside from 0-21 or 'any_str'),
    input function restarts, until he chooses the correct option."""
    while True:
        try:
            if ((font_index := int(input('\nSelect design number: ')))
                    not in options.keys()):
                print(error_color + 'Enter a number from 0 to 21...'
                      + reset_color)
                continue
        except (ValueError, TypeError):  # возвращаем в начало при ошибке ввода
            print(error_color + 'Invalid input. Please try again.'
                  + reset_color)
            continue

        return font_index


def add_color_option():
    """User selects Y or N option to color the text art
    If user enters wrong input - function restarts"""
    while ((add_color := input('Color the text? [y/n]: ').lower())
           not in 'yn' or len(add_color) == 0):
        print(error_color + 'Choose y or n.' + reset_color)
        continue
    else:
        return add_color


def print_color_menu():
    """Prints the menu of available colors for the text art.
    Collects data from colors dict."""
    for index, color_name in colors.items():
        print(f"{str(index):>3}. {color_name[0]:<15}",
              end=' ' if index % 2 == 1 else '\n')


def color_choice():
    """User selects the color of his choice for the text art to be colored.
    If user enters wrong input - function restarts"""
    while True:
        try:
            if ((color_index := int(input('Select color: ')))
                    not in colors):
                print(f'{error_color}Wrong color option. '
                      f'Please choose from 1 to 10.{reset_color}')
                continue
            return color_index

        except ValueError:
            print(f'{error_color}Invalid input. Please enter a number.'
                  f'{reset_color}')
            continue


def apply_color(text_art, color_index):
    """Applies color for the text art with color selected by user.
    Collects data for color from colors dict"""
    color = colors[color_index][1]

    return color + text_art + reset_color


def save_to_file_option():
    """Asks the user if he wants to save the result of Decor.font output
    Y or N option"""
    while ((save_choice := input('Save to file? [y/n]: ').lower())
           not in 'yn' or len(save_choice) == 0):
        print(f'{error_color}Choose y or n.{reset_color}')
        continue
    return save_choice


def save_to_file(art, font_name_index, color=False):
    """Saves the result of Decor.font output with additional strings
    (print({color} + r'''... and etc.) for a future usage in the code.
    Requires art, font_name_index, and (optional) color to execute."""
    if color is False:
        save(options[font_name_index][0], art)
        print('Done!', '\n')
    else:
        save(options[font_name_index][0], art, color)
        print('Done!', '\n')


def print_all_design():
    """All items option from the menu. Number 21.
    User inputs desired text and functions prints all 20 options of art.
    Every art is written in the res_list.
    After prints are completed, function saves all arts in the all_designs.txt
    """
    res_list = all_styles()
    for i in res_list:
        save('All_design', i)

    print('Saved to a file!\n', 'Done!', '\n')


def main():
    print_menu()
    while (choice := font_choice()) != 0:
        if choice == 21:  # All_items
            print_all_design()
            continue

        art = options[choice][1]()  # return art from Decor class

        if add_color_option() == 'y':
            print_color_menu()
            color_index = color_choice()
            colored_art = apply_color(art, color_index)

            print(f'\n{colored_art}')
            if save_to_file_option() == 'y':
                save_to_file(art, choice, colors[color_index][2])
        else:
            print(f'\n{art}')
            if save_to_file_option() == 'y':
                save_to_file(art, choice)

    print('Exit... Bye!')
    exit(0)  # if choice == 0


if __name__ == '__main__':
    logo = '''
 _____                             _             _____   _           _          _   
|_   _| __      __   ___   _ __   | |_   _   _  |  ___| (_)   __ _  | |   ___  | |_ 
  | |   \ \ /\ / /  / _ \ | '_ \  | __| | | | | | |_    | |  / _` | | |  / _ \ | __|
  | |    \ V  V /  |  __/ | | | | | |_  | |_| | |  _|   | | | (_| | | | |  __/ | |_ 
  |_|     \_/\_/    \___| |_| |_|  \__|  \__, | |_|     |_|  \__, | |_|  \___|  \__|
                                                |___/               |___/                  
        '''
    print(logo)

    options = {1: ('Digital', Dec.digital),
               2: ('Big', Dec.big),
               3: ('Bubble', Dec.bubble),
               4: ('Catwalk', Dec.catwalk),
               5: ('Chunky', Dec.chunky),
               6: ('Slant', Dec.slant),
               7: ('Doom', Dec.doom),
               8: ('Ogre', Dec.ogre),
               9: ('Rectangles', Dec.rectangles),
               10: ('Small', Dec.small),
               11: ('Smisome1', Dec.smisome1),
               12: ('Cybermedium', Dec.cybermedium),
               13: ('Cyberlarge', Dec.cyberlarge),
               14: ('Cybersmall', Dec.cybersmall),
               15: ('Drpepper', Dec.drpepper),
               16: ('Standard', Dec.standard),
               17: ('Graceful', Dec.graceful),
               18: ('Graffiti', Dec.graffiti),
               19: ('Fuzzy', Dec.fuzzy),
               20: ('Lean', Dec.lean),
               21: ('All items', ),
               0: ('Exit', )}

    colors = {1: ('red', '\033[31m', r'"\033[31m"'),
              2: ('green', '\033[32m', r'"\033[32m"'),
              3: ('orange', '\033[33m', r'"\033[33m"'),
              4: ('blue', '\033[34m', r'"\033[34m"'),
              5: ('purple', '\033[35m', r'"\033[35m"'),
              6: ('cyan', '\033[36m', r'"\033[36m"'),
              7: ('yellow', '\033[93m', r'"\033[93m"'),
              8: ('lightblue', '\033[94m', r'"\033[94m"'),
              9: ('pink', '\033[95m', r'"\033[95m"'),
              10: ('lightcyan', '\033[96m', r'"\033[96m"')}

    error_color = '\033[31m'
    reset_color = '\033[0m'
    try:
        main()
    except KeyboardInterrupt:
        print('\nProgram finished manually!')
        exit(0)
