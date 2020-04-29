"""
Command line interface for cross stitch pattern creation.
"""

import sys
import click

from crosstitch_helper.imagetool import ImageTool
from crosstitch_helper.stitch_counter import StitchCounter

from conf import palettes

@click.command()
@click.argument("image", type=click.File('rb'))
@click.argument("palette_name")
def stitchify(image, palette_name):
    """
    Create a cross-stitch pattern from IMAGE using PALETTE.

    Palette with the same name must be present in conf/palettes.py.
    """
    palette = getattr(palettes, palette_name, None)
    if not palette:
        click.echo("palette '{}' not found in conf/palettes.py".format(palette))
        sys.exit(1)

    image_tool = ImageTool(image)

    counter = StitchCounter(image_tool.iterate_pixels, palette)
    print(counter.stitch_count_string())


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    stitchify()
