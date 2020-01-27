import click

from ..admin import CQL, ACCEPTED
from ..conf import CONF, STATIC
from ..patron import PatronTester
from ..user import User


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def patron_group(ctx, debug):
    ctx.obj = {}
    ctx.obj["DEBUG"] = debug
    ctx.obj["CONF"] = CONF


@patron_group.command()
@click.pass_context
def test_new_patron_zero_sources(ctx):
    try:
        click.echo("\n\n====== Reset tables and make test user ======")
        CQL.reset()
        user = User()
        user.fully_register_rando()

        click.echo("\n\n====== Load customer from stripe ======")
        pt1 = PatronTester(user=user)
        ares = pt1.h_load_or_create_new_customer()
        sources = ares["b"]["patron"]["customer"]["sources"]
        stripe_id = ares["b"]["patron"]["stripeId"]
        click.echo(stripe_id)
        assert len(sources["data"]) == 0
        assert sources["total_count"] == 0
        assert len(stripe_id) > 4

        click.echo("Test passed")

    except Exception as err:
        raise err

    click.echo("Test complete")


@patron_group.command()
@click.pass_context
def test_patron_process_card_in_future(ctx):
    try:
        click.echo("\n\n====== Reset tables and make test user ======")
        CQL.reset()
        user = User()
        user.fully_register_rando()

        click.echo("\n\n====== Load customer from stripe ======")
        pt1 = PatronTester(user=user)
        ares = pt1.h_load_or_create_new_customer()
        sources = ares["b"]["patron"]["customer"]["sources"]
        stripe_id = ares["b"]["patron"]["stripeId"]
        click.echo(stripe_id)
        assert len(sources["data"]) == 0
        assert sources["total_count"] == 0
        assert len(stripe_id) > 4

        pt2 = PatronTester(user=user)
        pt2.stripe_id = stripe_id
        stripe_res = pt2.stripe_add_payment_method()
        print(stripe_res)

        click.echo("Test passed")

    except Exception as err:
        raise err

    click.echo("Test complete")
