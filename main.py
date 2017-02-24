import cyclos_api


if __name__ == "__main__":
    resp = cyclos_api.auth_data_for_login()
    print("resp"+resp.text)
    for resp_item in resp.json():
        print("resp_item")
        print(resp_item)
