import falcon
from src.helpers import getTrader

class Trader:

        def on_get(self, request, response, traderId):
            data = getTrader(traderId) # get all orders that match traderId
            retval = {
                'data': data
            }
            response.media = retval
            response.status = falcon.HTTP_200

