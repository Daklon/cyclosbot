import requests
from requests.auth import HTTPBasicAuth
import json


def _url(path):
    return 'https://communities.cyclos.org/tenerife/api/' + path


def authentication(name, password):
    return HTTPBasicAuth(name, password)


def auth_data_for_login():
    return requests.get(_url('auth/data-for-login'))


def get_account_balance(name, password):
    print("getting account balance for " + name)
    response = requests.get(_url(name+"/accounts"),
                            auth=authentication(name, password))
    # jsonStr = response.text
    # data = json.loads(jsonStr)
    data = response.json()
    return data
