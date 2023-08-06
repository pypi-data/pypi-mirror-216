class Color:
    generic_codes = {"reset": 0, "bold": 1, "italic": 3, "underline": 4,
                     "reverse": 7, "strikethrough": 9, "border": 51}

    class FG:
        fg_codes = {"black": 30, "red": 31, "green": 32, "orange": 33, "blue": 34,
                    "purple": 35, "cyan": 36, "lightgrey": 37, "darkgrey": 90,
                    "lightred": 91, "lightgreen": 92, "yellow": 93, "lightblue": 94,
                    "pink": 95, "lightcyan": 96, "white": 97}

    class BG:
        bg_codes = {"black": 40, "red": 41, "green": 42, "orange": 43, "blue": 44,
                    "purple": 45, "cyan": 46, "lightgrey": 47, "darkgrey": 100,
                    "lightred": 101, "lightgreen": 102, "yellow": 103, "lightblue": 104,
                    "pink": 105, "lightcyan": 106, "white": 107}


def make_color_method(code):
    def _method(text=""):
        return f"\033[{code}m{text}\033[0m"

    return _method


def apply_codes(obj, codes):
    for name in codes:
        _color_method = make_color_method(codes[name])
        setattr(obj, name, staticmethod(_color_method))


def coloreflection_init():
    apply_codes(Color, Color.generic_codes)
    apply_codes(Color.FG, Color.FG.fg_codes)
    apply_codes(Color.BG, Color.BG.bg_codes)
