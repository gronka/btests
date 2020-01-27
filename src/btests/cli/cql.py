import random

import click

from ..admin import CQL
from ..conf import CONF, NAMES, USER1, USER6, USER7, USER8
from ..user import User, create_user_from_dic
from ..search import Search


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cql_group(ctx, debug):
    ctx.obj = {}
    ctx.obj["DEBUG"] = debug
    ctx.obj["CONF"] = CONF


@cql_group.command()
@click.pass_context
def reset_tables(ctx):
    click.echo("\n\n====== Truncating tables ======")
    # TODO: make this be the admin user
    user = User()
    CQL.reset(user)
