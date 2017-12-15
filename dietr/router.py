from . import app

class Router:
    def __init__(self):
        self.routes = {}

    def register_route(self, route, methods = ['GET', 'POST']):
        def route_decorator(action):
            def wrapper(*args, **kwargs):
                # Set allowed methods
                action.methods = methods

                return action
            return wrapper
        return route_decorator

    def default_route(self):
        pass

    def resolve_route(self, path):
        pass

router = Router()

from .controllers.overview import OverviewController
