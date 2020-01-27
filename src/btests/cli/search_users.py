import random

import click

from ..admin import CQL
from ..conf import CONF, NAMES, USER1, USER6, USER7, USER8
from ..user import User, create_user_from_dic
from ..search import Search


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def search_users_group(ctx, debug):
    ctx.obj = {}
    ctx.obj["DEBUG"] = debug
    ctx.obj["CONF"] = CONF


@search_users_group.command()
@click.option(
    "-n",
    "--name",
    default="Barry",
    help=("Name to search for. Default: Barry")
)
@click.pass_context
def test_search_name(ctx, name):
    click.echo("\n\n====== Testing Name Search ======")
    CQL.reset()
    try:
        user6 = create_user_from_dic(USER6)
        user6.fully_register()
        user6.set_field("fullname", USER6["fullname"])

        user7 = create_user_from_dic(USER7)
        user7.fully_register()
        user7.set_field("fullname", USER7["fullname"])

        user8 = create_user_from_dic(USER8)
        user8.fully_register()
        user8.set_field("fullname", USER8["fullname"])

        tests = [
            {"name": "Barry", "expected_len": 2},
            {"name": "Barry Guy", "expected_len": 3},
            {"name": "dAN", "expected_len": 1},
            {"name": "BArry Denny Howard", "expected_len": 5},
        ]
        search = Search(user6)

        for test in tests:
            name = test["name"]
            expected_len = test["expected_len"]
            ares = search.search_by_name(name)
            results = ares["b"]["results"]
            assert len(results) == expected_len
            len_results = 0 if not results else len(results)
            search.log("search for {} returns {} results".format(name, len_results))

    except Exception as err:
        raise err

    finally:
        user6.remove()
        user7.remove()
        user8.remove()


@search_users_group.command()
@click.option(
    "-d",
    "--distance",
    default="15",
    help=("Search radius. Default: 15")
)
@click.pass_context
def test_search_nearest(ctx, distance):
    click.echo("\n\n====== Testing Nearest Search ======")
    CQL.reset()
    try:
        users = []
        locs = [
            {"lat": 35.80, "lng": -78.60},  # in Raleigh, dq25e
            {"lat": 35.80, "lng": -78.65},  # in Raleigh, dq25d
            {"lat": 35.80, "lng": -78.72},  # in Raleigh, dq258
            {"lat": 35.80, "lng": -78.77},  # in Raleigh, dnrgx
        ]

        for x in range(len(locs)):
            user = User()
            user.fully_register_rando()
            user.update_location(lat=locs[x]["lat"], lng=locs[x]["lng"])
            users.append(user)
            click.echo("added user")

        tests = [
            {"lat": 35.80, "lng": -78.65, "radius": 200, "expected_len": 3},
            {"lat": 35.80, "lng": -78.65, "radius": 40, "expected_len": 1},
            {"lat": 35.80, "lng": -78.65, "radius": 10, "expected_len": 0},
        ]
        search = Search(users[0])

        for test in tests:
            lat = test["lat"]
            lng = test["lng"]
            radius = test["radius"]
            expected_len = test["expected_len"]
            ares = search.search_by_nearest(lat, lng, radius)
            results = ares["b"]["results"]
            print(results)
            # assert len(results) == expected_len
            len_results = 0 if not results else len(results)
            search.log("search for radius {} at lat {} lng {} returns {} results".
                       format(radius, lat, lng, len_results))

    except Exception as err:
        raise err

    finally:
        click.echo("Removing users")
        for user in users:
            user.remove()
