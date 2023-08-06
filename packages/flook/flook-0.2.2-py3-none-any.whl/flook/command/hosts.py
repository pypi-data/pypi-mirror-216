# MIT License
#
# Copyright (c) 2023 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import click

from flook.model.host import Host
from flook.module.logger import Logger
from flook.module.database import Database
from flook.module.output import Output
from flook.module.config import Config


class Hosts:
    """Hosts Class"""

    def __init__(self):
        self.output = Output()
        self.database = Database()
        self.config = Config()
        self.logger = Logger().get_logger(__name__)

    def init(self):
        """Init database and configs"""
        self._configs = self.config.load()
        self.database.connect(self._configs["database"]["path"])
        self.database.migrate()
        return self

    def add(self, host):
        """Add a new host"""
        if self.database.get_host(host.name) is not None:
            raise click.ClickException(f"Host with name {host.name} exists")

        self.database.insert_host(host)

        click.echo(f"Host with name {host.name} got created")

    def list(self, tag, output):
        """List hosts"""
        data = []
        hosts = self.database.list_hosts()

        for host in hosts:
            if tag != "" and tag not in host.tags:
                continue

            data.append(
                {
                    "ID": host.id,
                    "Name": host.name,
                    "IP": host.ip,
                    "Connection": host.connection.upper(),
                    "Tags": ", ".join(host.tags) if len(host.tags) > 0 else "-",
                    "Created at": host.created_at,
                    "Updated at": host.updated_at,
                }
            )

        if len(data) == 0:
            raise click.ClickException(f"No hosts found!")

        print(
            self.output.render(
                data, Output.JSON if output.lower() == "json" else Output.DEFAULT
            )
        )

    def get(self, name, output):
        """Get a host"""
        host = self.database.get_host(name)

        if host is None:
            raise click.ClickException(f"Host with name {name} not found")

        data = [
            {
                "ID": host.id,
                "Name": host.name,
                "IP": host.ip,
                "Connection": host.connection.upper(),
                "Tags": ", ".join(host.tags) if len(host.tags) > 0 else "-",
                "Created at": host.created_at,
                "Updated at": host.updated_at,
            }
        ]

        print(
            self.output.render(
                data, Output.JSON if output.lower() == "json" else Output.DEFAULT
            )
        )

    def delete(self, name):
        """Delete a host"""
        self.database.delete_host(name)

        click.echo(f"Host with name {name} got deleted")
