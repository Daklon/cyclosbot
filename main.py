import cyclos_api


def main():
    resp = cyclos_api.auth_data_for_login()
    for resp_item in resp.json():
        print() 
