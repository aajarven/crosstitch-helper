"""
Command line interface for cross stitch pattern creation.
"""

import click

@click.command()
@click.argument("image")
@click.argument("palette")
def stitchify(image, palette):
    """
    Create a cross-stitch pattern from IMAGE using PALETTE.

    Palette with the same name must be present in conf/palette.py.
    """
    click.echo("stitchifying {} using {}".format(image, palette))

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    stitchify()
