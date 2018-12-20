import csv
import datetime
import os
import pandas as pd

LEDGER_PATH = "../data/ledger.csv"



class Entry:

    def __init__(self,traderId, order):
        self.traderId = traderId
        self.symbol = order['symbol']
        self.quantity = (order['quantity'])
        self.quantityRemaining = (order['quantity'])
        self.orderType = order['orderType']
        self.orderTime = datetime.datetime.now()
        self.status = 'open'


    def writeToLedger(self):
        # Update entries and current entry to be written
        self = update(self)
        # If file DNE, creates a new csv file with appropriate headers
        if (os.path.isfile(LEDGER_PATH) == False):
            headers = ['traderId', 'symbol','quantity','quantityRemaining','orderType','orderTime','status']
            with open(LEDGER_PATH, 'w') as ledger:
                writer = csv.DictWriter(ledger, fieldnames=headers)
                writer.writeheader()

        df = pd.read_csv(LEDGER_PATH)
        request = pd.DataFrame([[self.traderId, self.symbol, str(self.quantity), str(self.quantityRemaining),
                                 self.orderType, str(self.orderTime), self.status]], columns=list(df))
        df = df.append(request, ignore_index=True)

        f = open(LEDGER_PATH, "w+")
        df.to_csv(f, index=False)
        f.close()

    def getData(self):
        # Returns dict of current object
        if (self.quantityRemaining == 0):
            self.status = 'filled'
        content =  {
            'symbol': self.symbol,
            'quantity': self.quantity,
            'quantityRemaining': self.quantityRemaining,
            'orderType': self.orderType,
            'orderTime': str(self.orderTime),
            'status': self.status
        }
        return content




def update(entry):
    # If file DNE, we don't have to update entries
    if (os.path.isfile(LEDGER_PATH)):
        df = pd.read_csv(LEDGER_PATH)
        for i, row in df.iterrows():
            if entry.symbol == df.at[i,'symbol'] and df.at[i, 'traderId'] != entry.traderId and df.at[i, 'orderType'] != entry.orderType and int(df.at[i, 'quantityRemaining']) > 0 and int(entry.quantityRemaining) > 0:
                if int(df.at[i, 'quantityRemaining']) < int(entry.quantityRemaining):
                    temp = int(entry.quantityRemaining)
                    temp -= int(df.at[i, 'quantityRemaining'])
                    entry.quantityRemaining = temp
                    df.at[i, 'quantityRemaining'] = 0
                    df.at[i, 'status'] = 'filled'
                elif int(df.at[i, 'quantityRemaining']) > int(entry.quantityRemaining):
                    temp = int(entry.quantityRemaining)
                    df.at[i, 'quantityRemaining'] = int(df.at[i, 'quantityRemaining']) - temp
                    entry.quantityRemaining = 0
                    entry.status = 'filled'
                else:
                    df.at[i, 'quantityRemaining'] = 0
                    entry.quantityRemaining = 0
                    df.at[i, 'status'] = 'filled'
                    entry.status = 'filled'
        f = open(LEDGER_PATH, "w+")
        df.to_csv(f, index=False)
        f.close()

    return entry