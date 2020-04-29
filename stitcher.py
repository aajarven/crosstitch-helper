"""
Command line interface for cross stitch pattern creation.
"""

import sys
import click

from crosstitch_helper.imagetool import ImageTool

from conf import palettes

@click.command()
@click.argument("image", type=click.File('rb'))
@click.argument("palette")
def stitchify(image, palette):
    """
    Create a cross-stitch pattern from IMAGE using PALETTE.

    Palette with the same name must be present in conf/palettes.py.
    """
    colour_codes = getattr(palettes, palette, None)
    if not colour_codes:
        click.echo("palette '{}' not found in conf/palettes.py".format(palette))
        sys.exit(1)

    image_tool = ImageTool(image)
    for colour in image_tool.iterate_pixels():
        print(colour)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    stitchify()
