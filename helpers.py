import os

import requests

AUTHENTICATION_SERVICE_URL = "http://authentication:8000"


def system_user_auth():
    # Request to get token using system user
    system_user_data = {
        "username": os.environ.get("USER"),
        "password": os.environ.get("PASSWORD")
    }

    url = AUTHENTICATION_SERVICE_URL + "/api/token/"

    req = requests.post(url=url, data=system_user_data)
    response = req.json()
    system_user_token = response["access"]

    return system_user_token


def get_user_id_by_auth(user_id):

    system_user_token = system_user_auth()

    # Use system user token to make request
    auth_req = AUTHENTICATION_SERVICE_URL + f"/users/{user_id}"
    auth_header = {"Authorization": f"Bearer {system_user_token}"}
    auth_response = requests.get(url=auth_req, headers=auth_header)

    return auth_response
