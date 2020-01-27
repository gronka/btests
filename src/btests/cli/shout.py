import click

from ..admin import CQL, ACCEPTED
from ..conf import CONF
from ..shout import Shout
from ..user import User


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def shout_group(ctx, debug):
    ctx.obj = {}
    ctx.obj["DEBUG"] = debug
    ctx.obj["CONF"] = CONF


@shout_group.command()
@click.pass_context
def test_shout(ctx):
    CQL.reset()
    try:
        click.echo("\n\n====== Try to make a shout ======")
        shouter = User()
        shouter.fully_register_rando()

        shout = Shout(shouter=shouter)
        data = {
            "lat": CONF["lat01"],
            "lng": CONF["lng01"],
            "shoutTextNum": 1,
        }

        ares = shout.h_create_shout(data)
        assert ares["i"] == ACCEPTED

        click.echo("\n\n====== Try to find the shout ======")

        ares = shout.h_get_shouts_nearby(CONF["lat01"], CONF["lng01"], 40)
        print(ares)
        assert ares["i"] == ACCEPTED
        assert len(ares["b"]["results"]) == 1

        ares = shout.h_get_shouts_nearby(0, 0, 40)
        print(ares)
        assert ares["i"] == ACCEPTED
        assert ares["b"]["results"] is None


    except Exception as err:
        raise err

    click.echo("Test passed")
