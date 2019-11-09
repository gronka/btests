import random

import click

from ..admin import CQL
from ..conf import CONF, NAMES, USER1, USER6, USER7, USER8
from ..user import User, create_user_from_dic
from ..search import Search


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def user_group(ctx, debug):
    ctx.obj = {}
    ctx.obj["DEBUG"] = debug
    ctx.obj["CONF"] = CONF


@user_group.command()
@click.pass_context
def test_user_simple(ctx):
    click.echo("\n\n====== Testing User Api ======")
    CQL.reset()
    user = User()
    user.from_dic(USER6)
    user.setup_remove()
    user.test_signup()
    user.test_signup_duplicate()
    user.get_verify_code()
    user.test_verify_code_incorrect()
    user.test_verify_code_correct()
    user.test_remove()


@user_group.command()
@click.pass_context
def add_basic_users(ctx):
    click.echo("\n\n====== Adding predefined users ======")
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

    except Exception as err:
        raise err


@user_group.command()
@click.pass_context
def add_admin(ctx):
    click.echo("\n\n====== Adding admin user ======")
    try:
        user1 = create_user_from_dic(USER1)
        user1.fully_register()
        user1.set_field("fullname", USER1["fullname"])

    except Exception as err:
        raise err


@user_group.command()
@click.option(
    "-n",
    "--number",
    default="1",
    type=int,
    help=("Number of users to add. Default: 1")
)
@click.option(
    "-T",
    "--latrange",
    default="33.895782,36.198019",
    type=str,
    help=("lat range for user to be located in. Default spans Charlotte to Wilmington")
)
@click.option(
    "-G",
    "--lngrange",
    default="-77.479736,-81.257381",
    type=str,
    help=("lng range for user to be located in. Default spans most of NC")
)
@click.pass_context
def add_randos(ctx, number, latrange, lngrange):
    click.echo("\n\n====== Adding random user ======")
    lat_range = [float(x) for x in latrange.split(",")]
    lng_range = [float(x) for x in lngrange.split(",")]
    try:
        for i in range(number):
            user = User()
            user.fully_register_rando()
            fullname = "{} {} {}".format(random.choice(NAMES),
                                         random.choice(NAMES),
                                         random.choice(NAMES),
                                         )
            user.set_field("fullname", fullname)

            lat = random.uniform(lat_range[0], lat_range[1])
            lng = random.uniform(lng_range[0], lng_range[1])
            user.update_location(lat, lng)

    except Exception as err:
        raise err


# TODO: command to test setting good and bad values to fields
# TODO: installation id spam test
