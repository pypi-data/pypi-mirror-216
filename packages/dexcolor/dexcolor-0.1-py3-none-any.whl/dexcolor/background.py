class back:
    background_code = {
        'black': '40',
        'red': '41',
        'green': '42',
        'yellow': '43',
        'blue': '44',
        'magenta': '45',
        'cyan': '46',
        'white': '47',
        'reset': '0',
        'gray': '48;5;242',
        'orange': '48;5;202',
        'purple': '48;5;92',
        'pink': '48;5;204',
        'light_red': '48;5;196',
        'light_green': '48;5;82',
        'light_blue': '48;5;69',
        'light_yellow': '48;5;226',
        'light_magenta': '48;5;165',
        'light_cyan': '48;5;87',
        'light_gray': '48;5;253',
        'light_orange': '48;5;216',
        'light_purple': '48;5;141',
        'light_pink': '48;5;207',
        'dark_gray': '48;5;240',
        'dark_red': '48;5;88',
        'dark_green': '48;5;28',
        'dark_yellow': '48;5;94',
        'dark_blue': '48;5;18',
        'dark_magenta': '48;5;90',
        'dark_cyan': '48;5;30',
    }

    @classmethod
    def _color(cls, text, back=None):

        background_format = ''

        if back:
            background_code = cls.background_code.get(back, '0')
            background_format = f"\033[{background_code}m"


        return f"{background_format}{text}"

    @classmethod
    def black(cls, text):
        return cls._color(text, back='black')

    @classmethod
    def red(cls, text):
        return cls._color(text, back='red')

    @classmethod
    def green(cls, text):
        return cls._color(text, back='green')

    @classmethod
    def yellow(cls, text):
        return cls._color(text, back='yellow')

    @classmethod
    def blue(cls, text):
        return cls._color(text, back='blue')

    @classmethod
    def magenta(cls, text):
        return cls._color(text, back='magenta')

    @classmethod
    def cyan(cls, text):
        return cls._color(text, back='cyan')

    @classmethod
    def white(cls, text):
        return cls._color(text, back='white')

    @classmethod
    def gray(cls, text):
        return cls._color(text, back='gray')

    @classmethod
    def orange(cls, text):
        return cls._color(text, back='orange')

    @classmethod
    def purple(cls, text):
        return cls._color(text, back='purple')

    @classmethod
    def pink(cls, text):
        return cls._color(text, back='pink')

    @classmethod
    def light_red(cls, text):
        return cls._color(text, back='light_red')

    @classmethod
    def light_green(cls, text):
        return cls._color(text, back='light_green')

    @classmethod
    def light_blue(cls, text):
        return cls._color(text, back='light_blue')

    @classmethod
    def light_yellow(cls, text):
        return cls._color(text, back='light_yellow')

    @classmethod
    def light_magenta(cls, text):
        return cls._color(text, back='light_magenta')

    @classmethod
    def light_cyan(cls, text):
        return cls._color(text, back='light_cyan')

    @classmethod
    def light_gray(cls, text):
        return cls._color(text, back='light_gray')

    @classmethod
    def light_orange(cls, text):
        return cls._color(text, back='light_orange')

    @classmethod
    def light_purple(cls, text):
        return cls._color(text, back='light_purple')

    @classmethod
    def light_pink(cls, text):
        return cls._color(text, back='light_pink')

    @classmethod
    def dark_gray(cls, text):
        return cls._color(text, back='dark_gray')

    @classmethod
    def dark_red(cls, text):
        return cls._color(text, back='dark_red')

    @classmethod
    def dark_green(cls, text):
        return cls._color(text, back='dark_green')

    @classmethod
    def dark_yellow(cls, text):
        return cls._color(text, back='dark_yellow')

    @classmethod
    def dark_blue(cls, text):
        return cls._color(text, back='dark_blue')

    @classmethod
    def dark_magenta(cls, text):
        return cls._color(text, back='dark_magenta')

    @classmethod
    def dark_cyan(cls, text):
        return cls._color(text, back='dark_cyan')
