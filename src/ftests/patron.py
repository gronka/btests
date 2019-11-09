import json
import os

import click
import stripe

from .conf import API, ACCEPTED, REJECTED
from .tester import Tester


class PatronTester(Tester):
    def __init__(self, user):
        self.user = user
        self.stripe_id = None

        home_dir = os.path.expanduser("~")
        fpath = os.path.join(home_dir, "projects", "confs", "kapi", "scrt.json")
        with open(fpath) as f:
            data = json.load(f)
            stripe.api_key = data["str"]

    def h_load_or_create_new_customer(self):
        data = {}
        url = API + "/patron/get.stripeCustomer"
        ares = self.user.post(url, data)
        return ares

    def stripe_add_payment_method(self):
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": "4242424242424242",
                "exp_month": 12,
                "exp_year": 2020,
                "cvc": "123",
            }
        )

        click.echo(payment_method)

        attached_payment_method = stripe.PaymentMethod.attach(
            payment_method.id,
            customer=self.stripe_id
        )

        click.echo(attached_payment_method)
        # card = stripe.Customer.create_source(self.stripe_id, source="tok_amex")
