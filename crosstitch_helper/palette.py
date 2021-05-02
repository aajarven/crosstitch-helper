"""
Class for depicting floss palettes.
"""

import json

from colormath.color_objects import LabColor, sRGBColor
from colormath import color_conversions, color_diff
import numpy as np
from sklearn.neighbors import NearestNeighbors


class Palette():
    """
    Floss palette
    """

    _neighbor_graph = None
    _palette_size_at_update = -1

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

    def best_match(self, color):
        """
        Return the best matching floss color in the palette to the given color.

        :color: an array containing the RGB values (in range 0-255) of the
                color.
        """
        if self._palette_size_at_update != len(self.colors):
            self._update_neighbor_graph()
        rgbcolor = sRGBColor(*color, is_upscaled=True)
        labcolor = color_conversions.convert_color(rgbcolor, LabColor)
        _, indices = self._neighbor_graph.kneighbors(
                np.array([np.array(labcolor.get_value_tuple())]))
        return self.colors[indices[0][0]]

    def _update_neighbor_graph(self):
        """
        Recalculate the nearest neighbors tree.
        """
        def _cielab_color_distance(colorarray1, colorarray2):
            """
            Return the CIE 1994 color difference of the two given colors.

            The colors are provided as Numpy arrays containing the L, a and b
            coordinates of the color.
            """
            labcolor1 = LabColor(*colorarray1)
            labcolor2 = LabColor(*colorarray2)
            return color_diff.delta_e_cie1994(labcolor1, labcolor2,
                                              K_L=2, K_1=0.048, K_2=0.014)

        data = np.array([np.array(c) for c in self.colors])
        self._neighbor_graph = NearestNeighbors(n_neighbors=1,
                                                algorithm="ball_tree",
                                                metric=_cielab_color_distance
                                                ).fit(data)
        self._palette_size_at_update = len(self.colors)


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
        self._rgb = None
        self._lab = None

    @property
    def rgbcolor(self):
        """
        Return colormath.sRGBColor representation of the color
        """
        if not self._rgb:
            self._rgb = sRGBColor.new_from_rgb_hex(self.color)
        return self._rgb

    @property
    def labcolor(self):
        """
        Return colormath.LabColor representation of the color
        """
        if not self._lab:
            self._lab = color_conversions.convert_color(self.rgbcolor,
                                                        LabColor)
        return self._lab

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

    def __array__(self):
        """
        Return an array representation of the CIELab color of this floss.
        """
        return np.array(self.labcolor.get_value_tuple())
