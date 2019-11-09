from .conf import API, STATIC, ACCEPTED, REJECTED


class Shout:
    def __init__(self, shouter):
        self.shouter = shouter

    def h_create_shout(self, shout):
        url = API + "/shout/create"
        ares = self.shouter.post(url, shout)
        return ares

    def h_get_shouts_nearby(self, lat, lng, radius):
        url = API + "/shout/search.nearest"
        data = {
            "lat": lat,
            "lng": lng,
            "radius": radius,
        }
        ares = self.shouter.post(url, data)
        return ares

