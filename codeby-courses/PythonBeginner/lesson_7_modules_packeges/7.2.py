from example import str_examp
from colorama import init, Fore
init(autoreset=True)

print(str_examp.replace('#', Fore.GREEN + '#' + Fore.RESET))


print()


from example import str_examp
from colorama import init, Fore
init(autoreset=True)
for elem in str_examp:
    if elem == '#':
        elem = Fore.GREEN + elem
    print(elem, end='')