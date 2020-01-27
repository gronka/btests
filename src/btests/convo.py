from .conf import API, STATIC, ACCEPTED, REJECTED
from .tester import Tester


# TODO: maybe set a flag for if this request has been used, so each request
# can only be used once?
class ConvoTester(Tester):
    def __init__(self, user):
        self.user = user

        self.convo_uuid = None
        self.apparent_uuid = None
        # self.real_uuid = None
        self.datetime = None
        self.msg_uuid = None
        self.body = None
        self.last_msg_time = None
        self.new_last_msg_time = None
        self.participant_uuids = None
        self.participant_roles = None
        self.participant_hash = None

    def h_create(self):
        data = {
            "apparentUuid": self.apparent_uuid,
            "participantUuids": self.participant_uuids,
        }
        url = API + "/convo/create"
        ares = self.user.post(url, data)
        self._used = True
        return ares

    def h_get_recent_convos(self):
        data = {
            "apparentUuid": self.apparent_uuid,
        }
        url = API + "/convo/get.recent"
        ares = self.user.post(url, data)
        self._used = True
        return ares

    def h_send_msg(self):
        data = {
            "convoUuid": self.convo_uuid,
            "apparentUuid": self.apparent_uuid,
            "body": self.body,
        }
        url = API + "/convo/send"
        ares = self.user.post(url, data)
        self._used = True
        return ares

    def h_get_convo_msgs(self):
        data = {
            "convoUuid": self.convo_uuid,
            "apparentUuid": self.apparent_uuid,
        }
        print(data)
        url = API + "/convo/get.msgs"
        ares = self.user.post(url, data)
        self._used = True
        return ares
