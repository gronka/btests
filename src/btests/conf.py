# import pytest

STATIC = {
    "ACCEPTED": "ACCEPTED",
    "REJECTED": "REJECTED",
    "apiProtocol": "http",
    "apiHost": "127.0.0.1",
    "apiPort": "9090",
    "apiVersion": "v1",
    "timeout": 5,

    "uuidStringEmpty": "00000000-0000-0000-0000-000000000000",
    "uuidStringOne": "00000000-0000-0000-0000-000000000001",
    "uuidStringTwo": "00000000-0000-0000-0000-000000000002",
}

STATIC["api"] = "{}://{}:{}/{}".format(
    STATIC["apiProtocol"],
    STATIC["apiHost"],
    STATIC["apiPort"],
    STATIC["apiVersion"],
)

API = STATIC["api"]
ACCEPTED = STATIC["ACCEPTED"]
REJECTED = STATIC["REJECTED"]

CONF = {
    "lat_range": [ 42.4, 42.8 ],
    "lng_range": [ 20.9, 21.5 ],
    "lat01": 42.7,
    "lng01": 21.3,
}

USER1 = {
    "name": "user1",
    "fullname": "Admin User",
    "phoneOrEmail": "1",
    "password": "1",
    "callingCode": "1",
    "phoneCountryIso": "us",
    "installationId": "11",
}

USER6 = {
    "name": "user6",
    "fullname": "Barry Denny Guy",
    "phoneOrEmail": "6",
    "password": "6",
    "callingCode": "1",
    "phoneCountryIso": "us",
    "installationId": "66",
}

USER7 = {
    "name": "user7",
    "fullname": "Barry Denny Howard",
    "phoneOrEmail": "7",
    "password": "7",
    "callingCode": "1",
    "phoneCountryIso": "us",
    "installationId": "77",
}

USER8 = {
    "name": "user8",
    "fullname": "Spencer Dan Lewis",
    "phoneOrEmail": "8",
    "password": "8",
    "callingCode": "1",
    "phoneCountryIso": "us",
    "installationId": "88",
}

ADMIN = {
    "name": "user9",
    "fullname": "Terry Hacker",
    "phoneOrEmail": "9",
    "password": "9",
    "callingCode": "1",
    "phoneCountryIso": "us",
    "installationId": "99",
}

NAMES = [
    "Barry",
    "Henry",
    "David",
    "Devon",
    "Chris",
    "Jo",
    "Antoine",
    "Anthony",
    "Ben",
    "Emma",
    "Scarlett",
    "Martha",
    "Anna",
]
