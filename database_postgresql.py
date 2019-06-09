import psycopg2
from config import config

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


def create_table():
    """ create tables in the PostgreSQL database"""
    command = """
        CREATE TABLE trades (
            id SERIAL PRIMARY KEY,
            event_time INTEGER NOT NULL,
            symbol VARCHAR(255) NOT NULL,
            trade_id INTEGER NOT NULL,
            price DOUBLE PRECISION NOT NULL,
            quantity DOUBLE PRECISION NOT NULL,
            buyer INTEGER NOT NULL,
            seller INTEGER NOT NULL,
            trade_time INTEGER NOT NULL,
            is_market_maker BOOLEAN NOT NULL            
        )
        """
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# create_table()

def insert_trade(trade):
    """ insert a new trade into the vendors table """
    sql = """INSERT INTO trades(event_time,
                symbol,
                trade_id,
                price,
                quantity,
                buyer,
                seller,
                trade_time,
                is_market_maker)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING trade_id;"""
    conn = None
    vendor_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (trade['E'],
                          trade['s'],
                          trade['t'],
                          trade['p'],
                          trade['q'],
                          trade['b'],
                          trade['a'],
                          trade['T'],
                          trade['m']))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return vendor_id


# print(insert_trade(tradex))

# conn = psycopg2.connect(**config())
# cursor = conn.cursor()
#
# cursor.execute('SELECT * FROM trades LIMIT 10')
# records = cursor.fetchall()
# print(records)
#
# cursor.close()
# conn.close()
