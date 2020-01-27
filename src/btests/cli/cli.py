"""Collect cli commands here as an entrypoint
"""
import click

from .convo import convo_group
from .cql import cql_group
from .patron import patron_group
from .planner import planner_group
from .search_users import search_users_group
from .shout import shout_group
from .user import user_group


main = click.CommandCollection(sources=[
    convo_group,
    cql_group,
    patron_group,
    planner_group,
    search_users_group,
    shout_group,
    user_group,
])
