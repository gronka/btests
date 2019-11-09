import random

import click
import requests

from .conf import API, STATIC, ACCEPTED, REJECTED


def create_user_from_dic(dic):
    user = User()
    user.from_dic(dic)
    return user


class User:
    def __init__(self):
        self.name = "notset"
        self.user_uuid = "notset"
        self.phone_or_email = "notset"
        self.password = "notset"
        self.calling_code = "nostset"
        self.phone_country_iso = "notset"
        self.installation_id = "notset"

        self.lat = ""
        self.lng = ""

        self.code = ""
        # self.jwt = "notset"
        self.headers = {}
        self.timeout = STATIC["timeout"]

    def from_dic(self, dic):
        self.name = dic["name"]
        self.phone_or_email = dic["phoneOrEmail"]
        self.password = dic["password"]
        self.calling_code = dic["callingCode"]
        self.phone_country_iso = dic["phoneCountryIso"]
        self.installation_id = dic["installationId"]

    def post(self, url, data={}):
        with requests.Session() as session:
            res = session.post(url=url,
                               json=data,
                               headers=self.headers,
                               timeout=STATIC["timeout"])
            ares = res.json()
        return ares

    def set_field(self, field, value):
        url = API + "/user/field.update"
        data = {
            "itemUuid": self.user_uuid,
            "field": field,
            "value": value,
        }
        ares = self.post(url, data)
        return ares

    def update_location(self, lat, lng):
        self.lat = lat
        self.lng = lng

        url = API + "/user/location.update"
        data = {
            "lat": self.lat,
            "lng": self.lng,
        }
        ares = self.post(url, data)
        return ares

    def create_headers(self, jwt):
        self.headers = {"Authorization": jwt}

    def log(self, message):
        click.echo(self.name + ": " + message)

    def fully_register(self):
        self.setup_remove()
        self.signup()
        self.get_verify_code()
        self.try_verify_code(self.code)

    def fully_register_rando(self):
        rand = str(random.randint(1000, 9999))
        self.name = "user" + rand
        self.fullname = "User " + rand
        self.phone_or_email = rand
        self.password = rand
        self.calling_code = "1"
        self.phone_country_iso = "us"
        self.installation_id = rand

        self.setup_remove()
        self.signup()
        self.get_verify_code()
        self.try_verify_code(self.code)

    def signup(self):
        url = API + "/user/signup"
        data = {
            "phoneOrEmail": self.phone_or_email,
            "password": self.password,
            "callingCode": self.calling_code,
            "phoneCountryIso": self.phone_country_iso,
        }
        ares = self.post(url, data)

        # if key error occurs, user probably already exists
        # self.jwt = ares["b"]["jwt"]
        if ares["i"] == ACCEPTED:
            self.create_headers(ares["b"]["jwt"])
            self.user_uuid = ares["b"]["userUuid"]
            self.log("headers created")
        return ares

    def remove(self):
        url = API + "/user/remove"
        data = {
            "phoneOrEmail": self.phone_or_email,
            "phoneCountryIso": self.phone_country_iso,
        }
        ares = self.post(url, data)
        return ares

    def setup_remove(self):
        ares = self.remove()
        self.log("Attempting to delete user: ")
        if ares["i"] == ACCEPTED:
            self.log("----> user deleted")
        elif ares["i"] == REJECTED:
            self.log("----> user not found for deletion")
        else:
            self.log("----> ERROR: unknown response")

    def get_verify_code(self):
        url = API + "/verify/phone.createCode"
        data = {
            "installationId": self.installation_id,
        }
        ares = self.post(url, data)

        self.code = ares["b"]["code"]
        self.log("verification code generated: " + self.code)
        assert self.code

    def try_verify_code(self, code):
        url = API + "/verify/phone.checkCode"
        data = {
            "guess": code,
            "installationId": self.installation_id,
        }
        ares = self.post(url, data)
        if ares["i"] == ACCEPTED:
            self.log("verify code accepted")
        else:
            self.log("verify code rejected")

        return ares

    def test_signup(self):
        ares = self.signup()
        assert ares["i"] == ACCEPTED
        self.log("created")

    def test_signup_duplicate(self):
        ares = self.signup()
        assert ares["i"] == REJECTED
        self.log("duplicate rejected")

    def test_verify_code_incorrect(self):
        ares = self.try_verify_code("99999")  # code too long
        assert ares["i"] == REJECTED
        self.log("bad verification code rejected")

    def test_verify_code_correct(self):
        ares = self.try_verify_code(self.code)  # code too long
        assert ares["i"] == ACCEPTED
        self.log("good verification code accepted")

    def test_remove(self):
        ares = self.remove()
        assert ares["i"] == ACCEPTED
        self.log("successfully removed")
