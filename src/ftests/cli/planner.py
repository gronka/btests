import click

from ..admin import CQL
from ..conf import CONF, NAMES, USER1, USER6, USER7, USER8, ACCEPTED, REJECTED
from ..planner import Planner, PlannerRequest
from ..user import User


# TODO: tests
# request filled time
# -- request filled time with out of range warning
# -- request filled time with conflict warning
# accept filled time
# reject filled time
# personal vacation filled time



@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def planner_group(ctx, debug):
    ctx.obj = {}
    ctx.obj["DEBUG"] = debug
    ctx.obj["CONF"] = CONF


@planner_group.command()
@click.pass_context
def test_empty_planner(ctx):
    click.echo("\n\n====== Testing Planner Api ======")
    CQL.reset()
    try:
        trainer = User()
        trainer.fully_register_rando()

        planner = Planner(owner=trainer)
        data = {"user_uuid": user.user_uuid}
        ares = planner.h_get_planner_by_user_uuid(data)
        assert ares["i"] == ACCEPTED
        assert ares["b"]["planner"]["sunday"] == None
        assert ares["b"]["planner"]["monday"] == None
        assert ares["b"]["planner"]["tuesday"] == None
        assert ares["b"]["planner"]["wednesday"] == None
        assert ares["b"]["planner"]["thursday"] == None
        assert ares["b"]["planner"]["friday"] == None
        assert ares["b"]["planner"]["saturday"] == None

    except Exception as err:
        raise err

    click.echo("Test passed")


@planner_group.command()
@click.pass_context
def test_filled_time_accepted(ctx):
    click.echo("\n\n====== Testing Planner Api ======")
    CQL.reset()
    trainer = User()
    trainer.fully_register_rando()

    requestee = User()
    requestee.fully_register_rando()
    try:

        planner = Planner(owner=trainer)
        planner.t_request_static_filled_time(requestee)

        ares = planner.t_get_static_filled_time_range()
        assert ares["i"] == ACCEPTED

        ares = planner.t_get_static_filled_time_range()
        assert ares["i"] == ACCEPTED
        print(ares)
        appt_uuid = ares["b"]["filledTimes"]["filledTimes"][0]["apptUuid"]

    except Exception as err:
        raise err

    click.echo("Test part 01 passed")

    try:
        # accept the appointment
        data = {
            "ownerUuid": trainer.user_uuid,
            "dayOfYear": 250,
            "startMm": 540,
            "apptUuid": appt_uuid,
        }

        ares = planner.h_accept_filled_time(data)
        assert ares["i"] == ACCEPTED

        ares = planner.t_get_static_filled_time_range()
        assert ares["i"] == ACCEPTED

    except Exception as err:
        raise err

    click.echo("Test 02 passed")


@planner_group.command()
@click.pass_context
def test_filled_time_canceled_by_owner(ctx):
    click.echo("\n\n====== Testing Planner Api ======")
    CQL.reset()
    trainer = User()
    trainer.fully_register_rando()

    requestee = User()
    requestee.fully_register_rando()
    try:

        planner = Planner(owner=trainer)
        planner.t_request_static_filled_time(requestee)

        ares = planner.t_get_static_filled_time_range()
        assert ares["i"] == ACCEPTED

        ares = planner.t_get_static_filled_time_range()
        assert ares["i"] == ACCEPTED
        print(ares)
        appt_uuid = ares["b"]["filledTimes"]["filledTimes"][0]["apptUuid"]

    except Exception as err:
        raise err

    click.echo("Test part 01 passed")

    try:
        # cancel the appointment
        data = {
            "ownerUuid": trainer.user_uuid,
            "dayOfYear": 250,
            "startMm": 540,
            "apptUuid": appt_uuid,
        }

        ares = planner.h_cancel_filled_time(data, trainer)
        assert ares["i"] == ACCEPTED

        ares = planner.t_get_static_filled_time_range()
        assert ares["i"] == ACCEPTED
        print(ares)
        assert ares["b"]["filledTimes"]["filledTimes"][0]["status"] == "canceled"
        assert ares["b"]["filledTimes"]["filledTimes"][0]["canceledBy"] == "owner"

    except Exception as err:
        raise err

    click.echo("Test 02 passed")


@planner_group.command()
@click.pass_context
def test_filled_time_canceled_by_requestee(ctx):
    click.echo("\n\n====== Testing Planner Api ======")
    CQL.reset()
    trainer = User()
    trainer.fully_register_rando()

    requestee = User()
    requestee.fully_register_rando()
    try:

        planner = Planner(owner=trainer)
        planner.t_request_static_filled_time(requestee)

        ares = planner.t_get_static_filled_time_range()
        assert ares["i"] == ACCEPTED

        ares = planner.t_get_static_filled_time_range()
        assert ares["i"] == ACCEPTED
        print(ares)
        appt_uuid = ares["b"]["filledTimes"]["filledTimes"][0]["apptUuid"]

    except Exception as err:
        raise err

    click.echo("Test part 01 passed")

    try:
        # cancel the appointment
        data = {
            "ownerUuid": trainer.user_uuid,
            "dayOfYear": 250,
            "startMm": 540,
            "apptUuid": appt_uuid,
            "requesteeUuid": appt_uuid,
        }

        ares = planner.h_cancel_filled_time(data, requestee)
        assert ares["i"] == ACCEPTED

        ares = planner.t_get_static_filled_time_range()
        assert ares["i"] == ACCEPTED
        print(ares)
        assert ares["b"]["filledTimes"]["filledTimes"][0]["status"] == "canceled"
        assert ares["b"]["filledTimes"]["filledTimes"][0]["canceledBy"] == "requestee"

    except Exception as err:
        raise err

    click.echo("Test 02 passed")

@planner_group.command()
@click.pass_context
def test_filled_time_rejected(ctx):
    click.echo("\n\n====== Testing Planner Api ======")
    CQL.reset()
    trainer = User()
    trainer.fully_register_rando()

    requestee = User()
    requestee.fully_register_rando()
    try:
        planner = Planner(owner=trainer)
        planner.t_request_static_filled_time(requestee)

        ares = planner.t_get_static_filled_time_range()
        assert ares["i"] == ACCEPTED
        appt_uuid = ares["b"]["filledTimes"]["filledTimes"][0]["apptUuid"]

    except Exception as err:
        raise err

    click.echo("Test part 01 passed")

    try:
        # reject the appointment
        data = {
            "ownerUuid": trainer.user_uuid,
            "dayOfYear": 250,
            "startMm": 540,
            "apptUuid": appt_uuid,
        }

        ares = planner.h_reject_filled_time(data)
        assert ares["i"] == ACCEPTED

        ares = planner.t_get_static_filled_time_range()
        assert ares["i"] == ACCEPTED

    except Exception as err:
        raise err

    click.echo("Test 02 passed")

@planner_group.command()
@click.pass_context
def test_filled_time_simple(ctx):
    click.echo("\n\n====== Testing Planner Api ======")
    CQL.reset()
    try:
        trainer = User()
        trainer.fully_register_rando()

        requestee = User()
        requestee.fully_register_rando()

        planner = Planner(owner=trainer)
        data = {
            "ownerUuid": user.user_uuid,
            "dayOfYear": 250,
            "startMm": 540,
            "endMm": 600,
            "tzOffset": -300,
            "reason": "practice",
            "status": "requested",
            "requesteeUuid": requestee.user_uuid,
        }

        ares = planner.h_request_filled_time(data)
        assert ares["i"] == ACCEPTED

        data = {
            "ownerUuid": user.user_uuid,
            "dayOfYearStart": 248,
            "dayOfYearEnd": 252,
        }
        ares = planner.h_get_filled_times(data)
        assert ares["i"] == ACCEPTED

    except Exception as err:
        raise err

    click.echo("Test passed")


@planner_group.command()
@click.pass_context
def test_planner_full(ctx):
    click.echo("\n\n====== Testing Planner Api ======")
    CQL.reset()
    try:
        trainer = User()
        trainer.fully_register_rando()
        planner = Planner(owner=trainer)

        first = {
            "ownerUuid": planner.user.user_uuid,
            "availableUpdates": 0,
            "newAvailableTimes": [
                {
                    "weekday": 1,
                    "startMm": 540,
                    "endMm": 1020,
                    "tzOffset": -300,
                },

                {
                    "weekday": 6,
                    "startMm": 540,
                    "endMm": 720,
                    "tzOffset": -300,
                },

                {
                    "weekday": 6,
                    "startMm": 780,
                    "endMm": 1020,
                    "tzOffset": -300,
                },
            ],
        }

        ares = planner.h_update_available_times(first)
        assert ares["i"] == ACCEPTED

        data = {
            "ownerUuid": planner.user.user_uuid,
        }
        ares = planner.h_get_planner_by_user_uuid(data)
        assert ares["i"] == ACCEPTED
        assert ares["b"]["planner"]["sunday"] == None
        assert len(ares["b"]["planner"]["monday"]) == 1
        assert ares["b"]["planner"]["tuesday"] == None
        assert ares["b"]["planner"]["wednesday"] == None
        assert ares["b"]["planner"]["thursday"] == None
        assert ares["b"]["planner"]["friday"] == None
        assert len(ares["b"]["planner"]["saturday"]) == 2

    except Exception as err:
        raise err

    click.echo("Test part 01 passed")

    try:
        second = {
            "ownerUuid": planner.user.user_uuid,
            "availableUpdates": 1,
            "newAvailableTimes": [
                {
                    "weekday": 2,
                    "startMm": 540,
                    "endMm": 1020,
                    "tzOffset": -300,
                },

                {
                    "weekday": 2,
                    "startMm": 780,
                    "endMm": 1020,
                    "tzOffset": -300,
                },
            ],
            "deletedTimes": [
                {
                    "weekday": 1,
                    "startMm": 540,
                },

                {
                    "weekday": 6,
                    "startMm": 540,
                },
            ],
        }

        ares = planner.h_update_available_times(second)
        assert ares["i"] == ACCEPTED

        data = {
            "ownerUuid": planner.user.user_uuid,
        }
        ares = planner.h_get_planner_by_user_uuid(data)
        assert ares["i"] == ACCEPTED
        assert ares["b"]["planner"]["sunday"] == None
        assert ares["b"]["planner"]["monday"] == None
        assert len(ares["b"]["planner"]["tuesday"]) == 2
        assert ares["b"]["planner"]["wednesday"] == None
        assert ares["b"]["planner"]["thursday"] == None
        assert ares["b"]["planner"]["friday"] == None
        assert len(ares["b"]["planner"]["saturday"]) == 1

    except Exception as err:
        raise err

    click.echo("Test part 02 passed")


@planner_group.command()
@click.pass_context
def test_planner_wrong_available_updates(ctx):
    click.echo("\n\n====== Testing Planner Api ======")
    CQL.reset()
    try:
        trainer = User()
        trainer.fully_register_rando()
        planner = Planner(owner=trainer)
        data = {
            "ownerUuid": planner.user.user_uuid,
            "availableUpdates": 20,
            "newAvailableTimes": [
                {
                    "weekday": 1,
                    "startMm": 540,
                    "endMm": 1020,
                    "tzOffset": -300,
                },
            ],
        }
        ares = planner.h_update_available_times(data)
        assert ares["i"] == REJECTED

        data = {
            "ownerUuid": planner.user.user_uuid,
        }
        ares = planner.h_get_planner_by_user_uuid(data)
        assert ares["i"] == ACCEPTED
        assert ares["b"]["planner"]["sunday"] == None
        assert ares["b"]["planner"]["monday"] == None
        assert ares["b"]["planner"]["tuesday"] == None
        assert ares["b"]["planner"]["wednesday"] == None
        assert ares["b"]["planner"]["thursday"] == None
        assert ares["b"]["planner"]["friday"] == None
        assert ares["b"]["planner"]["saturday"] == None

    except Exception as err:
        raise err

    click.echo("Test passed")


@planner_group.command()
@click.pass_context
def test_planner_wrong_filled_updates(ctx):
    click.echo("\n\n====== Testing Planner Api ======")
    CQL.reset()
    try:
        trainer = User()
        trainer.fully_register_rando()
        planner = Planner(owner=trainer)
        data = {
            "ownerUuid": planner.user.user_uuid,
            "availableUpdates": 20,
            "newAvailableTimes": [
                {
                    "weekday": 1,
                    "startMm": 540,
                    "endMm": 1020,
                    "tzOffset": -300,
                },
            ],
        }
        ares = planner.h_update_available_times(data)
        assert ares["i"] == REJECTED

        data = {
            "ownerUuid": planner.user.user_uuid,
        }
        ares = planner.h_get_planner_by_user_uuid(data)
        assert ares["i"] == ACCEPTED
        assert ares["b"]["planner"]["sunday"] == None
        assert ares["b"]["planner"]["monday"] == None
        assert ares["b"]["planner"]["tuesday"] == None
        assert ares["b"]["planner"]["wednesday"] == None
        assert ares["b"]["planner"]["thursday"] == None
        assert ares["b"]["planner"]["friday"] == None
        assert ares["b"]["planner"]["saturday"] == None

    except Exception as err:
        raise err

    click.echo("Test passed")
