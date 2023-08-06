"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import click
import configparser
import os

from .commands.configure import configure_cmd
from .commands.generate import generate_cmd
from .commands.plan import plan_cmd
from .commands.events import events_cmd
from ._version import __version__


@click.group(chain=True)
@click.version_option(version=__version__, message="%(version)s")
@click.pass_context
def cli(ctx):
    """Command-line interface for the StellaNow SDK code generation and comparison tool."""
    # Create a new configparser object
    config = configparser.ConfigParser()

    # Get the home directory
    home = os.path.expanduser("~")

    # Read the configuration from a file in the .stellanow directory
    config.read(os.path.join(home, ".stellanow", "config.ini"))

    # Store the configuration in the context, so it can be accessed by other commands
    ctx.obj = config


cli.add_command(configure_cmd)
cli.add_command(generate_cmd)
cli.add_command(plan_cmd)
cli.add_command(events_cmd)
