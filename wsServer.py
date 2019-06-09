import json
import threading
import time

from simple_websocket_server import WebSocketServer, WebSocket

from database import select_buy_by_symbol, select_sell_by_symbol
from utils import get_preferences

pairs = get_preferences()['pairs']
symbol = {}
ths = {}
number = 500


def decrease(array):
    for x in array:
        x.pop('buyer')
        x.pop('seller')
        x.pop('event_time')
        x.pop('is_market_maker')
        x.pop('symbol')
        x.pop('trade_id')
        x.pop('trade_time')
    return array


class SimpleEcho(WebSocket):
    def update(self):
        while True:
            if symbol[self.address[1]] != '':
                buy_trades = decrease(select_buy_by_symbol(symbol[self.address[1]], number))
                sell_trades = decrease(select_sell_by_symbol(symbol[self.address[1]], number))
                print('{} Update chart: {} {}'.format(self.address[1],
                                                      symbol[self.address[1]],
                                                      json.dumps({"buy": buy_trades, "sell": sell_trades})))
                self.send_message(json.dumps({
                    "buy": buy_trades,
                    "sell": sell_trades
                }))
            time.sleep(1)

    def handle(self):
        global symbol
        if self.data in pairs:
            print('{} Select symbol: {}'.format(self.address[1], self.data))
            symbol[self.address[1]] = self.data.replace('_', '')

    def connected(self):
        global th
        global symbol
        symbol[self.address[1]] = ''
        print(self.address[1], 'connected')
        th = threading.Thread(target=self.update)
        ths[self.address[1]] = th
        th.start()

        self.send_message(json.dumps({"pairs": pairs}))

    def handle_close(self):
        print(self.address[1], 'closed')
        global ths
        global symbol
        symbol[self.address[1]] = ''
        ths[self.address[1]].kill()


server = WebSocketServer('', 9999, SimpleEcho)
server.serve_forever()
