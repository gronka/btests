import click

from ..admin import CQL, ACCEPTED
from ..conf import CONF, STATIC
from ..convo import ConvoTester
from ..user import User


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def convo_group(ctx, debug):
    ctx.obj = {}
    ctx.obj["DEBUG"] = debug
    ctx.obj["CONF"] = CONF


@convo_group.command()
@click.pass_context
def test_convo_create(ctx):
    try:
        click.echo("\n\n====== Reset tables and make test user ======")
        CQL.reset()
        user = User()
        user.fully_register_rando()

        click.echo("\n\n====== Try to make a convo ======")
        ct = ConvoTester(user=user)
        ct.apparent_uuid = user.user_uuid
        # TODO: test when apparent_uuid != user.user_uuid
        ct.participant_uuids = [user.user_uuid, STATIC["uuidStringOne"]]
        ares = ct.h_create()
        assert ares["i"] == ACCEPTED
        click.echo("convo created")

        click.echo("\n\n====== Try to find the convo ======")
        ct2 = ConvoTester(user=user)
        ct2.apparent_uuid = user.user_uuid
        # TODO: test when apparent_uuid != user.user_uuid
        ares = ct2.h_get_recent_convos()
        print(ares)
        assert ares["i"] == ACCEPTED

    except Exception as err:
        raise err

    click.echo("Test passed")


@convo_group.command()
@click.pass_context
def test_convo_full(ctx):
    try:
        click.echo("\n\n====== Reset tables and make test user ======")
        CQL.reset()
        user = User()
        user.fully_register_rando()

        ct = ConvoTester(user=user)
        click.echo("\n\n====== Try to make a convo ======")
        ct.apparent_uuid = user.user_uuid
        # TODO: test when apparent_uuid != user.user_uuid
        ct.participant_uuids = [user.user_uuid, STATIC["uuidStringOne"]]

        ares = ct.h_create()
        assert ares["i"] == ACCEPTED
        click.echo("convo created")

        ct2 = ConvoTester(user=user)
        click.echo("\n\n====== Try to find the convo ======")
        ct2.apparent_uuid = user.user_uuid
        # TODO: test when apparent_uuid != user.user_uuid
        ares2 = ct2.h_get_recent_convos()

        assert ares2["i"] == ACCEPTED
        assert len(ares2["b"]["results"]) == 1
        click.echo("one convo found")

        ct3 = ConvoTester(user=user)
        click.echo("\n\n====== Send a msg to new convo ======")
        ct3.convo_uuid = ares2["b"]["results"][0]["convoUuid"]
        ct3.apparent_uuid = user.user_uuid
        ct3.body = "Very nice!"

        ares3 = ct3.h_send_msg()
        print(ares3)
        assert ares3["i"] == ACCEPTED
        click.echo("message posted")

        ct4 = ConvoTester(user=user)
        click.echo("\n\n====== Get convo msgs ======")
        ct4.convo_uuid = ares2["b"]["results"][0]["convoUuid"]
        ct4.apparent_uuid = user.user_uuid

        ares4 = ct4.h_get_convo_msgs()
        print(ares4)
        assert ares4["i"] == ACCEPTED
        click.echo("one msg found")

    except Exception as err:
        raise err

    click.echo("Test passed")
