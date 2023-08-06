class RainbowText:
    @staticmethod
    def dex(text, start_color, middle_color, end_color):
        start_rgb = name_to_rgb(start_color)
        middle_rgb = name_to_rgb(middle_color)
        end_rgb = name_to_rgb(end_color)

        text_length = len(text)
        middle_ratio = 1 / (text_length - 1)

        colored_text = ""
        for i, char in enumerate(text):
            if i == 0:
                color = start_rgb
            elif i == text_length - 1:
                color = end_rgb
            else:
                color = blend_colors(start_rgb, end_rgb, middle_ratio * i)

            colored_text += colorize_text(char, color)

        return colored_text

def name_to_rgb(color_name):
    color_name = color_name.lower()
    if color_name == "black":
        return (0, 0, 0)
    elif color_name == "red":
        return (255, 0, 0)
    elif color_name == "green":
        return (0, 255, 0)
    elif color_name == "yellow":
        return (255, 255, 0)
    elif color_name == "blue":
        return (0, 0, 255)
    elif color_name == "magenta":
        return (255, 0, 255)
    elif color_name == "cyan":
        return (0, 255, 255)
    elif color_name == "white":
        return (255, 255, 255)
    elif color_name == "gray":
        return (128, 128, 128)
    elif color_name == "orange":
        return (255, 165, 0)
    elif color_name == "purple":
        return (128, 0, 128)
    elif color_name == "pink":
        return (255, 192, 203)
    elif color_name == "light_red":
        return (255, 102, 102)
    elif color_name == "light_green":
        return (102, 255, 102)
    elif color_name == "light_blue":
        return (102, 178, 255)
    elif color_name == "light_yellow":
        return (255, 255, 102)
    elif color_name == "light_magenta":
        return (255, 102, 255)
    elif color_name == "light_cyan":
        return (102, 255, 255)
    elif color_name == "light_gray":
        return (192, 192, 192)
    elif color_name == "light_orange":
        return (255, 204, 102)
    elif color_name == "light_purple":
        return (204, 102, 255)
    elif color_name == "light_pink":
        return (255, 204, 229)
    elif color_name == "dark_gray":
        return (64, 64, 64)
    elif color_name == "dark_red":
        return (128, 0, 0)
    elif color_name == "dark_green":
        return (0, 128, 0)
    elif color_name == "dark_yellow":
        return (128, 128, 0)
    elif color_name == "dark_blue":
        return (0, 0, 128)
    elif color_name == "dark_magenta":
        return (128, 0, 128)
    elif color_name == "dark_cyan":
        return (0, 128, 128)

def blend_colors(color1, color2, ratio):
    blended_color = tuple(int(c1 * ratio + c2 * (1 - ratio)) for c1, c2 in zip(color1, color2))
    return blended_color

def colorize_text(text, rgb_color):
    return f"\033[38;2;{rgb_color[0]};{rgb_color[1]};{rgb_color[2]}m{text}\033[0m"
