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

def send_order(request):
    symbol = request.symbol
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        return None
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
    if not mt5.symbol_select(symbol,True):
        print("symbol_select({}}) failed, exit",symbol)
        return None

    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 1,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100*point,
        "tp": price + 100*point,
        "deviation": 10,
        "magic": 234000,
        "comment": "python script",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)

    if result is None:
        print('No result info')
        return None
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))

    return { 'result': result, 'request': request, 'point': point }


def shutdown():
    mt5.shutdown()