import csv
import json
import pandas as pd
from .entry import Entry
import os
LEDGER_PATH = "../data/ledger.csv"

def getDataList(list):
    content = {
        'symbol': list[0],
        'quantity': list[1],
        'quantityRemaining': list[2],
        'orderType': list[3],
        'orderTime': list[4],
        'status': list[5]
        }
    return content

# Used for debugging
def readFromLedger():
    with open(LEDGER_PATH, mode='r') as ledger:
        reader = csv.reader(ledger, delimiter = ',', quotechar='"')
        data = []
        for row in reader:
            entry = Entry(row[0], getDataList(row[1:7]))
            data.append(entry.getData())

        ledger.close()
        return json.dumps(data, default = str)

def getTrader(trader):
    with open(LEDGER_PATH, mode='r') as ledger:
        reader = csv.reader(ledger, delimiter = ',', quotechar='"')
        orders = []

        for row in reader:
            if row[0] == trader:
                entry = Entry(trader, getDataList(row[1:7]))
                data = entry.getData()
                del data['quantityRemaining'] # Sample Model excludes this attribute
                orders.append(data)
        return orders
