import cyclos_api
import config


if __name__ == "__main__":
    data = cyclos_api.get_account_balance(config.NAME, config.PASSWORD)
    print(data)
