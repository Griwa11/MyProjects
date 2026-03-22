from twenty.all_scripts.design import Decor as Dec

options = {
    1: Dec.digital,
    2: Dec.big,
    3: Dec.bubble,
    4: Dec.catwalk,
    5: Dec.chunky,
    6: Dec.slant,
    7: Dec.doom,
    8: Dec.ogre,
    9: Dec.rectangles,
    10: Dec.small,
    11: Dec.smisome1,
    12: Dec.cybermedium,
    13: Dec.cyberlarge,
    14: Dec.cybersmall,
    15: Dec.drpepper,
    16: Dec.standard,
    17: Dec.graceful,
    18: Dec.graffiti,
    19: Dec.fuzzy,
    20: Dec.lean}


def all_styles():
    text = Dec.get_text()

    res_list = []
    for option in options:
        art = options[option](text)
        res_list.append(art)
        print(art)

    return res_list
