import falcon
from src.health_check import HealthCheck
from src.trader import Trader
from src.orders import Orders

APP = falcon.API()

health_check_resource = HealthCheck()
APP.add_route('/health', health_check_resource)

orders_resource = Orders()
APP.add_route('/orders', orders_resource)

trader_resource = Trader()
APP.add_route('/orders/{traderId}', trader_resource)
