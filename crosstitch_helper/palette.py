"""
Class for depicting floss palettes.
"""

import json


class Palette():
    """
    Floss palette
    """

    def __init__(self, colors=None):
        """
        Create a new palette

        :colors: Optional list of `FlossColor`s to include in the palette
        """
        if not colors:
            self.colors = []
        else:
            self.colors = colors

    @classmethod
    def load(cls, file_path):
        """
        Return a palette read from a JSON file saved using the `save` method.
        """
        with open(file_path) as jsonfile:
            color_list = json.load(jsonfile)
        colors = []
        for color in color_list:
            colors.append(FlossColor(**color))
        return cls(colors)

    def save(self, file_path, indent=4):
        """
        Save the palette to a JSON file.

        Colors are saved in a list, each color represented as a dictionary.

        :file_path: Location of the output file
        :indent: Indentation depth in the output file. Defaults to 4.
        """
        dicts = [c.to_dict() for c in self.colors]
        with open(file_path, "w") as outfile:
            outfile.write(json.dumps(dicts, indent=indent))


class FlossColor():
    """
    Representation of a specific floss.
    """

    def __init__(self, color, symbol="x", symbol_color="#000000",
                 color_number="", color_name=""):
        """
        Initialize the color

        :color: The hex value of the color, e.g. "#838a29"
        :symbol: The symbol used for the color in charts. Defaults to "x"
                 unless given.
        :symbol_color: Color used when drawing the symbol. E.g. ("#000000")
        :color_number: Floss color chart number, e.g. "DMC 581".
        :color_name: Floss color name, e.g. "Moss Green"
        """
        # pylint: disable=too-many-arguments
        self.color = color
        self.symbol = symbol
        self.symbol_color = symbol_color
        self.color_number = color_number
        self.color_name = color_name

    def __repr__(self):
        """
        Return a string representation of the color.

        For example:
        #EFF4A4 ⛬   DMC 165 Moss Green Very Light
        """
        return ("{color} {symbol}\t{number}\t{name}"
                "".format(color=self.color,
                          symbol=self.symbol,
                          number=self.color_number,
                          name=self.color_name))

    def __eq__(self, color):
        """
        Two colors are equal if they have the same color code.
        """
        if not isinstance(color, self.__class__):
            return False
        return self.color == color.color

    def to_dict(self):
        """
        Return a dictionary representation of the class
        """
        return {"color": self.color,
                "symbol": self.symbol,
                "symbol_color": self.symbol_color,
                "color_number": self.color_number,
                "color_name": self.color_name,
                }
