
class StitchCounter():
    """
    A class for determining stitch stats.
    """

    def __init__(self, stitch_iterator, palette):
        """
        Create a new StitchCounter instance.

        :stitch_iterator: iterator that yields hex strings for each stitch in
                          the pattern
        :palette: colour palette that holds the symbols for each colour
        """
        self._stitch_iterator = stitch_iterator
        self._palette = palette
        self.stitch_count = {}

    def count_all_stitches(self):
        """
        Count stitches of each colour.

        The result is stored in self.stitch_count. If stitches have already
        been counted, nothing is done.
        """
        if not self.stitch_count:
            self.stitch_count = {}
            for hexvalue in self._stitch_iterator():
                if hexvalue not in self._palette:
                    raise ValueError("Colour {} found in the pattern image, not "
                                     "found in the colour palette."
                                     "".format(hexvalue))
                self._add_stitch(hexvalue)

    def _needs_stitch_count(func, *args, **kwargs):
        """
        Decorator for functions that need to have the stitch count calculated
        before runnign them.
        """
        # pylint: disable=no-self-argument, not-callable
        def wrapper(self):
            self.count_all_stitches()
            return func(self, *args, **kwargs)
        return wrapper

    @_needs_stitch_count
    def stitch_count_string(self):
        """
        Return a string that represents the numbers of stitches in each colour.

        Each colour is on its own line, the most prevalent colour first.
        Colours are identified using the symbols specified in the palette.
        """

        def sorter(colour):
            return self.stitch_count_for_colour(colour)

        lines = ["{}\t{}".format(self._palette[colour][0],
                                 self.stitch_count[colour])
                 for colour in
                 sorted(self.stitch_count, key=sorter, reverse=True)]
        return "\n".join(lines)


    def _add_stitch(self, hexvalue):
        """
        Increase the stitch count of a colour by one.

        :hexvalue: the colour for which the count is increased
        """
        if hexvalue in self.stitch_count:
            self.stitch_count[hexvalue] = self.stitch_count[hexvalue] + 1
        else:
            self.stitch_count[hexvalue] = 1

    def stitch_count_for_colour(self, colour):
        """
        Return the number of stitches of a colour in the pattern.

        :colour: hex value for the colour of interest
        """
        return self.stitch_count.get(colour, 0)
