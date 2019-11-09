from .conf import API, STATIC, ACCEPTED, REJECTED


class PlannerRequest:
    def __init__(self, **kargs):
        self.owner_uuid = kargs["owner_uuid"]
        self.day_of_year_start = kargs["day_of_year_start"]
        self.day_of_year_end = kargs["day_of_year_end"]
        self.weekday = kargs["weekday"]
        self.start_mm = kargs["start_mm"]
        self.end_mm = kargs["end_mm"]
        self.tz_offset = kargs["tz_offset"]


class Planner:
    def __init__(self, owner):
        self.owner = owner
        self.owner_uuid = self.owner.user_uuid

    def h_get_planner_by_owner_uuid(self, data):
        url = API + "/planner/by.ownerUuid"
        ares = self.owner.post(url, data)
        return ares

    def h_get_filled_times(self, data):
        url = API + "/planner/get.filledTimes"
        ares = self.owner.post(url, data)
        return ares

    def h_update_available_times(self, available_times):
        url = API + "/planner/update.availableTimes"
        ares = self.owner.post(url, available_times)
        return ares

    def h_get_planner_updates(self, pl):
        url = API + "/planner/get.updates"
        data = {
            "ownerUuid": pl.owner_uuid,
        }
        ares = self.owner.post(url, data)
        return ares

    def h_request_filled_time(self, data):
        url = API + "/planner/request.filledTime"
        ares = self.owner.post(url, data)
        return ares

    def h_reject_filled_time(self, data):
        url = API + "/planner/reject.filledTime"
        ares = self.owner.post(url, data)
        return ares

    def h_accept_filled_time(self, data):
        url = API + "/planner/accept.filledTime"
        ares = self.owner.post(url, data)
        return ares

    def h_cancel_filled_time(self, data, user):
        url = API + "/planner/cancel.filledTime"
        ares = user.post(url, data)
        return ares

    def t_request_static_filled_time(self, requestee):
        url = API + "/planner/request.filledTime"
        data = {
            "ownerUuid": self.owner.user_uuid,
            "dayOfYear": 250,
            "startMm": 540,
            "endMm": 600,
            "tzOffset": -300,
            "reason": "practice",
            "status": "requested",
            "requesteeUuid": requestee.user_uuid,
        }
        ares = self.owner.post(url, data)
        return ares

    def t_get_static_filled_time_range(self):
        url = API + "/planner/get.filledTimes"
        data = {
            "ownerUuid": self.owner.user_uuid,
            "dayOfYearStart": 248,
            "dayOfYearEnd": 252,
        }
        print(data)
        ares = self.owner.post(url, data)
        return ares
