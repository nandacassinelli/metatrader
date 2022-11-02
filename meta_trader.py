import MetaTrader5 as mt5
import os
from operator import itemgetter
from dotenv import load_dotenv

load_dotenv()

def initialize():
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    return True

def login(credentials = False):
    if credentials:
        account, password, server = itemgetter('account', 'password', 'server')(credentials)
    account = int(os.getenv('LOGIN'))
    password = os.getenv('PASSWORD')
    server = os.getenv('SERVER')

    authorized= mt5.login(account, password, server)
    if not authorized:
        print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
        return False
    return True

def get_account_info(props = False):
    account_info_dict = mt5.account_info()._asdict()
    if not props:
        return account_info_dict
    info = {}
    for prop in props:
        info[prop] = account_info_dict[prop]
    return info

def shutdown():
    mt5.shutdown()