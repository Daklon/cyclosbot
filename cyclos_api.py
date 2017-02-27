import requests
from requests.auth import HTTPBasicAuth


# function that return the url where the api is
def _url(path):
    return 'https://communities.cyclos.org/tenerife/api/' + path


# Return the data needed by request auth param
def authentication(name, password):
    return HTTPBasicAuth(name, password)


# Return the auth data for login (now only used for testing pourposes)
def auth_data_for_login():
    return requests.get(_url('auth/data-for-login'))


# Return the account balance, it need the username and the password
def get_account_balance(name, password):
    response = requests.get(_url(name+"/accounts"),
                            auth=authentication(name, password))
    data = response.json()
    return data[0]['status']
    # return data
