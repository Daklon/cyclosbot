import requests
from requests.auth import HTTPBasicAuth


def _url(path):
    return 'https://communities.cyclos.org/tenerife/api/' + path


def authentication(name, password):
    return HTTPBasicAuth(name, password)


def auth_data_for_login():
    return requests.get(_url('auth/data-for-login'))


def get_account_balance(name, password):
    response = requests.get(_url(name+"/accounts"),
                            auth=authentication(name, password))
    data = response.json()
    return data[0]['status']
    # return data
