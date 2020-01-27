import random

import click
import requests

from .conf import API, STATIC, ACCEPTED, REJECTED, ADMIN
from .user import create_user_from_dic


class Database:
    def __init__(self):
        self.admin = create_user_from_dic(ADMIN)

    def reset(self):
        self.truncate_all_tables()

    def truncate_all_tables(self):
        url = API + "/admin/truncate.all"
        ares = self.admin.post(url)
        return ares


CQL = Database()
