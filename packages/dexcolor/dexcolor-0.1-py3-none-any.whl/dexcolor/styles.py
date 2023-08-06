class style:
    __style_code = {
        'reset': '0',
        'bold': '1',
        'dim': '2',
        'italic': '3',
        'underline': '4',
        'blink': '5',
        'blink_slow': '6',
        'reverse': '7',
        'overline': '53',
    }

    __reset_color = {
        'reset': '\033[0m'
    }

    @classmethod
    def _color(cls, text, style=None):
        style_format = ''

        if style:
            style_codes = [cls.__style_code.get(s, '0') for s in style.split()]
            style_format = ';'.join(style_codes)
            style_format = f"\033[{style_format}m"

        return f"{style_format}{text}"

    @classmethod
    def bold(cls, text):
        return cls._color(text, style='bold')
    
    @classmethod
    def dim(cls, text):
        return cls._color(text, style='dim')
    
    @classmethod
    def italic(cls, text):
        return cls._color(text, style='italic')
    
    @classmethod
    def underline(cls, text):
        return cls._color(text, style='underline')
    
    @classmethod
    def blink(cls, text):
        return cls._color(text, style='blink')
    
    @classmethod
    def blink_slow(cls, text):
        return cls._color(text, style='blink_slow')
    
    @classmethod
    def overline(cls, text):
        return cls._color(text, style='overline')
    
    @classmethod
    def reverse(cls, text):
        return cls._color(text, style='reverse')
    
    @classmethod
    def bold_italic(cls, text):
        return cls._color(text, style='bold italic')
    
    @classmethod
    def bold_dim(cls, text):
        return cls._color(text, style='bold dim')