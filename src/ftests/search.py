import click
import requests

from .conf import API, STATIC, ACCEPTED, REJECTED


class Search:
    def __init__(self, user):
        self.user = user

    def log(self, message):
        message = "search: " + str(message)
        self.user.log(message)

    def search_by_name(self, name):
        url = API + "/search/users/name"
        data = {
            "name": name,
        }
        ares = self.user.post(url, data)
        return ares

    def search_by_nearest(self, lat, lng, radius):
        url = API + "/search/users/nearest"
        data = {
            "lat": lat,
            "lng": lng,
            "radius": radius,
        }
        ares = self.user.post(url, data)
        return ares
        # assert ares["i"] == ACCEPTED
