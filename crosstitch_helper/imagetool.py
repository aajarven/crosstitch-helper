"""
Tools for working with pattern image
"""

from imageio import imread

from matplotlib.colors import to_hex


class ImageTool():
    """
    A tool for handling image data.
    """

    def __init__(self, path):
        """
        Create a new instance.

        :path: the input image, where one pixel corresponds to one stitch
        """
        self.path = path
        self._imagedata = imread(self.path, pilmode="RGB")

    def colour_values(self):
        """
        Return image colour data.
        """
        return self._imagedata

    def iterate_pixels(self):
        """
        Iterate over all pixels in the image, yielding hex value of each pixel.

        Covers the image row by row, from upper left to lower right.
        """
        for i in range(self._imagedata.shape[0]):
            for j in range(self._imagedata.shape[1]):
                yield to_hex(self._imagedata[i, j]/255.0)
