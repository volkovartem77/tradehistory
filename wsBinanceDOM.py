# import sys
# sys.path.append('/root/thbot')
import json
import time
import traceback

import websocket
from pymemcache.client.base import Client

from database import insert_trade
from utils import get_preferences

name = 'Binance'
client = Client(('127.0.0.1', 11211))
tt = 0


def on_message(ws, message):
    try:
        global tt
        data = json.loads(message)['data']
        symbol = data['s']

        insert_trade(data)
        print(symbol, data)

        # now = time.time()
        # print(round(now - tt, 5))
        # tt = time.time()

    except KeyboardInterrupt:
        pass
    except:
        print(traceback.format_exc())


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print('### opened ###')


while True:
    print('start websocket {}'.format(name))
    time.sleep(1)

    pairs = get_preferences()['pairs']
    print(pairs)

    try:
        subs = ''
        for pair in pairs:
            subs += pair.replace('_', '').lower() + '@trade/'
        if subs != '':
            print(subs)
            ws = websocket.WebSocketApp(
                "wss://stream.binance.com:9443/stream?streams={}".format(subs.strip('/')),
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close)
            ws.run_forever()
    except:
        print('ws{} Error: websocket failed'.format(name))
        print(traceback.format_exc())
