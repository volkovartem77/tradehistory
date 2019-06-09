import datetime
import json
import time

from database import insert_trade
from pymemcache.client.base import Client

client = Client(('127.0.0.1', 11211))

tradex = {
    "e": "trade",  # Event type
    "E": 123456789,  # Event time
    "s": "BNBBTC",  # Symbol
    "t": 12345,  # Trade ID
    "p": "0.001",  # Price
    "q": "100",  # Quantity
    "b": 88,  # Buyer order ID
    "a": 50,  # Seller order ID
    "T": 123456785,  # Trade time
    "m": True,  # Is the buyer the market maker?
    "M": True  # Ignore
}


def write_to_data_base(trade, n):
    data = 'data'
    json_body = [
        {
            "measurement": "tradeEvent",
            "tags": {
                "symbol": trade['s']
            },
            "time": datetime.datetime.utcnow().isoformat().split('.')[0] + 'Z',
            "fields": {
                "event_time": trade['E'],
                "trade_id": trade['t'],
                "price": trade['p'],
                "quantity": trade['q'],
                "buyer": trade['b'],
                "seller": trade['a'],
                "trade_time": trade['T'],
                "is_market_maker": trade['m']
            }
        }]
    data = insert_trade(json_body)
    print('{} INSERT {} {}'.format(n, data, trade))


def write_to_memcache(trade, n):
    current = client.get(trade['s'])
    if current is not None:
        current = json.loads(current)
    else:
        current = []
    current.append(trade)
    client.set(trade['s'], json.dumps(current))
    print('{} MEMCACHED {} {}'.format(n, len(current), current))


def test():
    n = 0

    while True:
        write_to_data_base(tradex, n)
        # write_to_memcache(tradex, n)
        n += 1
        # time.sleep(2)


test()

print(client.get('BNBBTC'))