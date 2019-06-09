import datetime

from influxdb import InfluxDBClient

name = 'storage'
client = InfluxDBClient(host='localhost', port=8086)
# client.create_database(name)
client.switch_database(name)


def insert_trade(trade):
    json_body = [
        {
            "measurement": "tradeEvent",
            "tags": {
                "symbol": trade['s']
            },
            "time": datetime.datetime.now().isoformat().split('.')[0] + 'Z',
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
    client.write_points(json_body)


def select_by_symbol(symbol, n):
    series = client.query("""SELECT * FROM "storage"."autogen"."tradeEvent" WHERE "symbol"='""" + symbol + "'")
    return list(series['tradeEvent'])[-n:]


def select_buy_by_symbol(symbol, n):
    series = client.query("""SELECT * FROM "storage"."autogen"."tradeEvent" WHERE "symbol"='""" + symbol + "'" +
                          """ and "is_market_maker"=false""")
    return list(series['tradeEvent'])[-n:]


def select_sell_by_symbol(symbol, n):
    series = client.query("""SELECT * FROM "storage"."autogen"."tradeEvent" WHERE "symbol"='""" + symbol + "'" +
                          """ and "is_market_maker"=true""")
    return list(series['tradeEvent'])[-n:]


# print(select_by_symbol('ETHBTC', 3))
# print(select_buy_by_symbol('MATICUSDT', 50))
# print(select_sell_by_symbol('MATICUSDT', 50))

# tradex = {
#     "e": "trade",  # Event type
#     "E": 123456789,  # Event time
#     "s": "BNBBTC",  # Symbol
#     "t": 12345,  # Trade ID
#     "p": "0.001",  # Price
#     "q": "100",  # Quantity
#     "b": 88,  # Buyer order ID
#     "a": 50,  # Seller order ID
#     "T": 123456785,  # Trade time
#     "m": True,  # Is the buyer the market maker?
#     "M": True  # Ignore
# }
#
# print(insert_trade(tradex))
# print(client.query('SELECT * FROM "storage"."autogen"."tradeEvent"').raw)
# print(results.raw)
# print(results.get_points(tags={'user':'Carol'}))
