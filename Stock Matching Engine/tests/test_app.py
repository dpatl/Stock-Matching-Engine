from src.helpers import getTrader
from src.entry import Entry
import pandas as pd
import os
LEDGER_PATH = "../data/ledger.csv"

ORDER1 = \
    {
        'traderId': 'deep',
        'orders': [
            {
                'symbol': 'AAPL',
                'quantity': 75,
                'orderType': 'sell'
            },
            {
                'symbol': 'SBUX',
                'quantity': 100,
                'orderType': 'buy'
            }
        ]
    }


ORDER2 = \
    {
        'traderId': 'shallow',
        'orders': [
            {
                'symbol': 'AAPL',
                'quantity': 100,
                'orderType': 'buy'
            },
            {
                'symbol': 'IBM',
                'quantity': 250,
                'orderType': 'buy'
            }
        ]
    }


ORDER3 = \
    {
        'traderId': 'bot',
        'orders': [
            {
                'symbol': 'AAPL',
                'quantity': 25,
                'orderType': 'buy'
            },
            {
                'symbol': 'IBM',
                'quantity': 250,
                'orderType': 'sell'
            },
            {
                'symbol': 'SBUX',
                'quantity': 200,
                'orderType': 'sell'
            }
        ]
    }

ORDER4 = \
    {
        'traderId': 'Shallow',
        'orders': [
            {
                'symbol': 'AAPL',
                'quantity': 21,
                'orderType': 'buy'
            }
        ]
    }

def test_write():
    orders = ORDER4['orders']
    traderId = ORDER4['traderId']
    for order in orders:
        entry = Entry(traderId, order)
        entry.writeToLedger()
        df = pd.read_csv(LEDGER_PATH)
        row = df.head(0)  # read first row ( this ignores header)
        for i, row in df.iterrows():
            assert df.at[i, 'traderId'] == traderId
            assert df.at[i, 'symbol'] == order['symbol']
            assert df.at[i, 'quantity'] == order['quantity']
            assert int(df.at[i, 'quantityRemaining']) == order['quantity'] # quantity should equal quantity remaining for only 1 order in ledger
            assert df.at[i, 'orderType'] == order['orderType']

    os.remove(LEDGER_PATH) # remove file so it what we did in this test doesn't affect other tests


def test_trader(trader):
    orders = ORDER1['orders']
    traderId = ORDER1['traderId']
    for order in orders:
        entry = Entry(traderId, order)
        entry.writeToLedger()

    # Write another order from with a different traderId to ensure only orders with specified traderId are returned
    orders = ORDER2['orders']
    traderId = ORDER2['traderId']

    for order in orders:
        entry = Entry(traderId, order)
        entry.writeToLedger()

    # So our ledger has 4 entries,but there's 2 traders with 2 orders each
    data = getTrader(trader)

    assert data[0]['symbol'] == ORDER1['orders'][0]['symbol']
    assert int(data[0]['quantity']) == ORDER1['orders'][0]['quantity']
    assert data[1]['symbol'] == ORDER1['orders'][1]['symbol']
    assert int(data[1]['quantity']) == ORDER1['orders'][1]['quantity']
    assert len(data) == 2 # Only 2 orders for traderId named 'deep'
    os.remove(LEDGER_PATH) # remove file so it what we did in this test doesn't affect other tests

def test_update(file):
    orders = ORDER1['orders']
    traderId = ORDER1['traderId']
    for order in orders:
        entry = Entry(traderId, order)
        entry.writeToLedger()

    orders = ORDER3['orders']
    traderId = ORDER3['traderId']

    for order in orders:
        entry = Entry(traderId, order)
        entry.writeToLedger()

    # ORDER1 has a buy for SBUX for 100 shares and ORDER3 has a sell for SBUX for quantity 200 =>
    # order from ORDER1 containing SBUX should be filled and ORDER3's withstanding shares should be 100 (from 200)
    df = pd.read_csv(LEDGER_PATH)
    for i, row in df.iterrows():
        if df.at[i, 'symbol'] == 'SBUX':
            assert df.at[i, 'quantity'] != df.at[i, 'quantityRemaining']
            if df.at[i, 'orderType'] == 'sell': # This is ORDER3 because it has a sell order for SBUX for 200 shares
                assert int(df.at[i, 'quantity']) == 200 # quantity should never change in ledger
                assert int(df.at[i, 'quantityRemaining']) == 100 # quantity remaining should change
            else:
                # This is ORDER1 because it had a buy order for SBUX that should have been fulfiled by ORDER3
                assert int(df.at[i, 'quantity']) == 100
                assert int(df.at[i, 'quantityRemaining']) == 0
                assert df.at[i, 'status'] == 'filled' # if quantity remaining is 0, status is filled
        elif df.at[i, 'symbol'] == 'AAPL':
            if df.at[i, 'orderType'] == 'sell': # This is ORDER1 because it has a sell order for AAPL for 75 shares
                assert int(df.at[i, 'quantity']) == 75 # quantity should never change in ledger
                assert int(df.at[i, 'quantityRemaining']) == 50 # quantity remaining should change
            else:
                # This is ORDER3 because it had a buy order for AAPL that should have been fulfiled by ORDER1
                assert int(df.at[i, 'quantity']) == 25
                assert int(df.at[i, 'quantityRemaining']) == 0
                assert df.at[i, 'status'] == 'filled' # if quantity remaining is 0, status is filled

    os.remove(LEDGER_PATH) # remove file so it what we did in this test doesn't interfere other tests




