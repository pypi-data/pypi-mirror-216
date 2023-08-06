class DEX:
    __color_code = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
        'reset': '0',
        'orange': '38;5;208',
        'purple': '38;5;129',
        'pink': '38;5;198',
        'light_red': '38;5;196',
        'light_green': '38;5;82',
        'light_blue': '38;5;69',
        'light_yellow': '38;5;226',
        'light_magenta': '38;5;165',
        'light_cyan': '38;5;87',
        'light_gray': '38;5;252',
        'light_orange': '38;5;216',
        'light_purple': '38;5;141',
        'light_pink': '38;5;207',
        'dark_gray': '38;5;240',
        'dark_red': '38;5;88',
        'dark_green': '38;5;28',
        'dark_yellow': '38;5;94',
        'dark_blue': '38;5;18',
        'dark_magenta': '38;5;90',
        'dark_cyan': '38;5;30',
    }

    __background_code = {
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

    __style_code = {
        'reset': '0',
        'bold': '1',
        'dim': '2',
        'italic': '3',
        'underline': '4',
        'blink': '5',
        'blink_slow': '6',
        'reverse': '7',
        'hidden': '8',
        'strikethrough': '9',
        'overline': '53',
    }

    @classmethod
    def _color(cls, text, color=None, back=None, style=None):
        color_format = ''
        background_format = ''
        style_format = ''

        if color:
            color_code = cls.__color_code.get(color, '37')
            color_format = f"\033[{color_code}m"

        if back:
            background_code = cls.__background_code.get(back, '0')
            background_format = f"\033[{background_code}m"

        if style:
            style_codes = [cls.__style_code.get(s, '0') for s in style.split()]
            style_format = ';'.join(style_codes)
            style_format = f"\033[{style_format}m"

        return f"{color_format}{background_format}{style_format}{text}"

    @classmethod
    def red(cls, text, style=None, back=None):
        return cls._color(text, color='red', style=style, back=back)

    @classmethod
    def green(cls, text, style=None, back=None):
        return cls._color(text, color='green', style=style, back=back)

    @classmethod
    def blue(cls, text, style=None, back=None):
        return cls._color(text, color='blue', style=style, back=back)

    @classmethod
    def black(cls, text, style=None, back=None):
        return cls._color(text, color='black', style=style, back=back)

    @classmethod
    def magenta(cls, text, style=None, back=None):
        return cls._color(text, color='magenta', style=style, back=back)

    @classmethod
    def cyan(cls, text, style=None, back=None):
        return cls._color(text, color='cyan', style=style, back=back)

    @classmethod
    def yellow(cls, text, style=None, back=None):
        return cls._color(text, color='yellow', style=style, back=back)

    @classmethod
    def white(cls, text, style=None, back=None):
        return cls._color(text, color='white', style=style, back=back)

    @classmethod
    def pink(cls, text, style=None, back=None):
        return cls._color(text, color='pink', style=style, back=back)

    @classmethod
    def purple(cls, text, style=None, back=None):
        return cls._color(text, color='purple', style=style, back=back)

    @classmethod
    def orange(cls, text, style=None, back=None):
        return cls._color(text, color='orange', style=style, back=back)

    @classmethod
    def dark_gray(cls, text, style=None, back=None):
        return cls._color(text, color='dark_gray', style=style, back=back)

    @classmethod
    def dark_red(cls, text, style=None, back=None):
        return cls._color(text, color='dark_red', style=style, back=back)

    @classmethod
    def dark_green(cls, text, style=None, back=None):
        return cls._color(text, color='dark_green', style=style, back=back)

    @classmethod
    def dark_yellow(cls, text, style=None, back=None):
        return cls._color(text, color='dark_yellow', style=style, back=back)

    @classmethod
    def dark_blue(cls, text, style=None, back=None):
        return cls._color(text, color='dark_blue', style=style, back=back)

    @classmethod
    def dark_magenta(cls, text, style=None, back=None):
        return cls._color(text, color='dark_magenta', style=style, back=back)

    @classmethod
    def dark_cyan(cls, text, style=None, back=None):
        return cls._color(text, color='dark_cyan', style=style, back=back)

    @classmethod
    def light_orange(cls, text, style=None, back=None):
        return cls._color(text, color='light_orange', style=style, back=back)

    @classmethod
    def light_purple(cls, text, style=None, back=None):
        return cls._color(text, color='light_purple', style=style, back=back)

    @classmethod
    def light_pink(cls, text, style=None, back=None):
        return cls._color(text, color='light_pink', style=style, back=back)

    @classmethod
    def light_gray(cls, text, style=None, back=None):
        return cls._color(text, color='light_gray', style=style, back=back)

    @classmethod
    def light_red(cls, text, style=None, back=None):
        return cls._color(text, color='light_red', style=style, back=back)

    @classmethod
    def light_green(cls, text, style=None, back=None):
        return cls._color(text, color='light_green', style=style, back=back)

    @classmethod
    def light_blue(cls, text, style=None, back=None):
        return cls._color(text, color='light_blue', style=style, back=back)

    @classmethod
    def light_yellow(cls, text, style=None, back=None):
        return cls._color(text, color='light_yellow', style=style, back=back)

    @classmethod
    def light_magenta(cls, text, style=None, back=None):
        return cls._color(text, color='light_magenta', style=style, back=back)

    @classmethod
    def light_cyan(cls, text, style=None, back=None):
        return cls._color(text, color='light_cyan', style=style, back=back)


RESET = '\033[0m'
