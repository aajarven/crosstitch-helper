"""
Command line interface for cross stitch pattern creation.
"""

import math
import sys
import click

from crosstitch_helper.imagetool import ImageTool
from crosstitch_helper.stitch_counter import StitchCounter

from conf import palettes

@click.command()
@click.argument("image", type=click.File('rb'))
@click.argument("palette_name")
@click.option("--stitches-per-skein", type=int, default=1700,
              help="How many stitches can one skein of thread make")
def stitchify(image, palette_name, stitches_per_skein):
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

    click.echo("Stitch counts for each colour:")
    click.echo(counter.stitch_count_string())

    click.echo()
    click.echo("Skein counts for each colour for {} stitches/skein:"
               "".format(stitches_per_skein))
    for colour in counter.stitch_count:
        click.echo("{}\t{}".format(
            palette[colour][0],
            math.ceil(1.0 * counter.stitch_count[colour]/stitches_per_skein)))

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    stitchify()
