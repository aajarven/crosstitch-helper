"""
Tool for automatically generating palettes
"""

import pprint


class PaletteCreator():
    """
    Create a palette for an image.
    """

    def __init__(self, stitch_iterator, symbols):
        """
        Create a new PaletteCreator.

        :stitch_iterator: An iterator that yields hex strings for each stitch
                          in the pattern.
        """
        self._stitch_iterator = stitch_iterator
        self._symbols = symbols
        self._palette = None

    def create_palette(self):
        """
        Determine the colours in the piece and their symbols.
        """
        self._palette = {}
        symbol_index = 0
        for hexvalue in self._stitch_iterator():
            if hexvalue not in self._palette:
                self._palette[hexvalue] = (self._symbols[symbol_index],
                                           "#000000")
                symbol_index += 1
                if symbol_index >= len(self._symbols):
                    symbol_index = 0

    def needs_palette(func, *args, **kwargs):
        """
        Decorator for functions that need to have the palette created before
        running.
        """
        # pylint: disable=no-self-argument, protected-access, not-callable
        def wrapper(self):
            if not self._palette:
                self.create_palette()
            return func(self, *args, **kwargs)
        return wrapper

    @needs_palette
    def palette_string(self):
        """
        Return a string representation of the palette.
        """
        printer = pprint.PrettyPrinter(indent=4)
        return printer.pformat(self._palette)
