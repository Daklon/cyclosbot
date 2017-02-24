import requests


def _url(path):
    print("_url")
    return 'https://demo.cyclos.org/api/' + path


def auth_data_for_login():
    print("get")
    return requests.get(_url('auth/data-for-login'))
