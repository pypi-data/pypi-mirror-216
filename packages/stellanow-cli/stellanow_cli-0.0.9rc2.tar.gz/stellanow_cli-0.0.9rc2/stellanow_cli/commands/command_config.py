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

import importlib
import click
import functools
import logging
import os

from ..api import StellaAPI
from ..config.int import ConfigInt
from ..config import Env
from ..utils.logger import setup_logger
from ..utils.utils import snake_to_camel


logger = logging.getLogger(__name__)


def common_option(f):
    """
    Common CLI options to be used across multiple commands
    """
    decorators = [
        click.option('--access_key',
                     help="The access key credential for accessing the StellaNow API. "
                          "This should be the same as your StellaNow account access key."),
        click.option('--access_token', hide_input=True,
                     help="The access token credential for accessing the StellaNow API. "
                          "This should be the same as your StellaNow account access token."),
        click.option('--organization_id',
                     help="The unique identifier (UUID) of the organization in StellaNow. "
                          "This is used to scope the operations within the given organization's context."),
        click.option('--project_id',
                     help="The unique identifier (UUID) of the project in StellaNow. "
                          "This is used to scope the operations within the given project's context."),
        click.option('--profile', default='DEFAULT',
                     help="The profile name for storing a particular set of configurations. "
                          "If no profile is specified, the configurations will be stored under the 'DEFAULT' profile."),
        click.option('--env', hidden=True, type=click.Choice([e.value for e in Env], case_sensitive=False), help=""),
        click.option('--verbose', '-v', is_flag=True, help="Enables verbose mode, which outputs more detailed logging "
                                                           "messages.")
    ]

    for decorator in reversed(decorators):
        f = decorator(f)
    return f


def load_config(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()

        profile = kwargs.get("profile", "DEFAULT")

        env_vars = {
            "access_key": os.getenv('STELLANOW_ACCESS_KEY'),
            "access_token": os.getenv('STELLANOW_ACCESS_TOKEN'),
        }

        for key in ["access_key", "access_token", "organization_id", "project_id", "profile", "env"]:
            # Check environment variables first
            if key in env_vars and env_vars[key] is not None:
                kwargs[key] = env_vars[key]
            # If not set in environment, check command options
            elif key not in kwargs or kwargs[key] is None:
                kwargs[key] = ctx.obj.get(profile, key, fallback=None)

        if kwargs['env'] is None:
            kwargs['env'] = "Nil"

        setup_logger(kwargs.get('verbose'))

        # Check if all required options are present
        if any(value is None for value in kwargs.values()):
            logger.error('All required options are not set. Please use the "configure" command to set them.')
            ctx.exit(1)

        env_config_class_name = f"Config{snake_to_camel(kwargs.get('env'))}"
        try:
            env_config_class = getattr(importlib.import_module(f"stellanow_cli.config.{kwargs.get('env')}"),
                                       env_config_class_name)
        except ImportError:
            env_config_class = ConfigInt

        # Create StellaAPI instance and pass it as a named argument
        kwargs['stella_api'] = StellaAPI(
            env_config_class(),
            kwargs.get('access_key'),
            kwargs.get('access_token'),
            kwargs.get('organization_id'),
            kwargs.get('project_id')
        )

        return ctx.invoke(f, *args, **kwargs)

    return wrapper
