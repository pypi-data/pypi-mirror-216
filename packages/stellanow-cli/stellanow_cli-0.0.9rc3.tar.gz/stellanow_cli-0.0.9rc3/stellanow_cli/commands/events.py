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

from prettytable import PrettyTable

from .command_config import common_option, load_config


@click.command(name='events')
@common_option
@load_config
@click.pass_context
def events(ctx, stella_api, organization_id, project_id, **kwargs):
    """Fetches the latest event specifications from the API and output a list of the events into the terminal prompt."""

    click.echo(f"\n\nOrganizationId: {organization_id}\nProjectId: {project_id}\n\n")

    _events = stella_api.get_events()

    table = PrettyTable(['EventID', 'Event Name', "Is Active", "Created At", "Updated At"])

    # Populate the table with data from your SkippedFile instances
    for event in _events:
        table.add_row([event.id, event.name, event.isActive, event.createdAt, event.updatedAt])

    click.echo(table)

    for event in _events:
        click.echo(f'ID: {event.id}, Name: {event.name}')


events_cmd = events
