import requests
from requests.auth import HTTPBasicAuth
import config


# function that return the url where the api is
def _url(path):
    return ('https://communities.cyclos.org/' + config.COMMUNITY
            + '/api/' + path)


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


# Return the basic account info
def auth(name, password):
    response = requests.get(_url('auth'),
                            auth=authentication(name, password))
    if (response.status_code == 200):
        return True
    else:
        return False


# Search advertisements
def search(name, password, keyword):
    pass


# Create new advertisement
def create(name, password, data):
    response = requests.post(_url(name+'/marketplace'),
                             json=data,
                             auth=authentication(name, password))
    if (response.status_code == 200):
        return True
    else:
        return False


# Get info needed to create new advertisements
def get_marketplace_info(name, password):
    payload = {'fields': 'categories', 'kind': 'simple'}
    # payload = {'kind': 'simple'}
    response = requests.get(_url(name+'/marketplace/data-for-new'),
                            params=payload,
                            auth=authentication(name, password))
    return response.json()
