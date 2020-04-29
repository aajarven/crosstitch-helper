"""
Palettes for different cross stitch projects.

Palettes are dicts, having the hex value of the colour as the key, and values
consisting of (symbol, fontcolour) pairs, where symbol is a single character
and fontcolour is the hex representation of the font used to print that
character when the base colour is the colour itself.
"""

monkey_island_palette = {
    '#000000': ('K', '#cecece'),
    '#555555': ('G', '#efefef'),
    '#aaaaaa': ('g', '#1c1c1c'),
    '#ffffff': ('W', '#000000'),
    '#0000aa': ('B', '#ffffff'),
    '#5555ff': ('b', '#ffffff'),
    '#00aaaa': ('T', '#ffffff'),
    '#55ffff': ('t', '#000000'),
    '#ffff55': ('Y', '#000000'),
    '#aa5500': ('C', '#000000'),
    '#aa00aa': ('V', '#000000'),
    '#ff5555': ('P', '#000000')
}

test_palette = {
    "#000000": ("k", "#ffffff"),
    "#ffffff": ("w", "#000000"),
    "#ff0000": ("r", "#000000"),
    "#00ff00": ("g", "#000000"),
    "#0000ff": ("b", "#000000"),
    "#ff00ff": ("p", "#000000"),
}
