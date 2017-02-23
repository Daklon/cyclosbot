import request


def _url(path):
    return 'https://demo.cyclos.org/api/' + path


def auth_data_for_login():
    return request.get(_url('auth/data-for-login'))
