from twenty.all_scripts.api import text_art


class Decor:
    @staticmethod
    def input_correction(user_input):
        if (not user_input.isascii()
                or len(user_input) == 0
                or len(user_input) > 30):
            print('\033[31m' + 'Text must be ASCII and between 1 '
                                   'and 30 characters long.' + '\033[0m')
            return None
        else:
            return user_input

    @staticmethod
    def get_text():
        while (text := Decor.input_correction(input('Enter text: '))) is None:
            continue

        return text

    @staticmethod
    def digital(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'digital')

    @staticmethod
    def big(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'big')

    @staticmethod
    def bubble(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'bubble')

    @staticmethod
    def catwalk(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'catwalk')

    @staticmethod
    def chunky(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'chunky')

    @staticmethod
    def slant(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'slant')

    @staticmethod
    def doom(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'doom')

    @staticmethod
    def ogre(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'ogre')

    @staticmethod
    def rectangles(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'rectangles')

    @staticmethod
    def small(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'small')

    @staticmethod
    def smisome1(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'smisome1')

    @staticmethod
    def cybermedium(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'cybermedium')

    @staticmethod
    def cyberlarge(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'cyberlarge')

    @staticmethod
    def cybersmall(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'cybersmall')

    @staticmethod
    def drpepper(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'drpepper')

    @staticmethod
    def standard(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'standard')

    @staticmethod
    def graceful(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'graceful')

    @staticmethod
    def graffiti(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'graffiti')

    @staticmethod
    def fuzzy(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'fuzzy')

    @staticmethod
    def lean(text=False):
        if text is False:
            text = Decor.get_text()
        return text_art(text, 'lean')