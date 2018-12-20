import falcon
import json
from .entry import Entry

class Orders:
    def on_post(self, request, response):

        data = json.loads(request.stream.read())

        traderId = data['data']['traderId']
        orders = data['data']['orders']

        # for each order, create an Entry object and write entry to the ledger
        for order in orders:
            entry = Entry(traderId, order)
            entry.writeToLedger()


        retval = {
                'data': {
                    'trader_id': traderId,
                    'orders': orders
                }
        }

        response.status = falcon.HTTP_200
        response.media = retval

