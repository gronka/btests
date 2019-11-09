import click


class Tester:
    def __init__(self):
        self._used = False

    def __getattribute__(self, attr):
        method = object.__getattribute__(self, attr)
        if attr == "_used":
            if callable(method):
                if self._used:
                    click.echo("!!!!!! This object cannot be called again")
                    return
        return method
