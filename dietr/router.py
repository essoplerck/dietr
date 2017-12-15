from . import app

class Router:
    def __init__(self):
        self.routes = {}

    def register_route(self, route, methods = ['GET', 'POST']):
        pass



    def default_route(self):
        pass

    def resolve_route(self, path):
        pass

router = Router()

from .controllers.overview import OverviewController
