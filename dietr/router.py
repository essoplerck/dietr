import re

from . import app

class Router:
    def __init__(self):
        self.routes = {}

        # Intercept all requests
        @app.route('/')
        @app.route('/<path:path>')
        def resolve_route(path = ''):
            return self.resolve_route(path)

    def register_route(self, url, action, methods = ['GET', 'POST']):
        # Compile regular expression
        route = re.compile(f'^{url}$')

        self.routes[route] = action

    def default_route(self):
        pass

    def resolve_route(self, path):
        # Add leading slash for path
        path = f'/{path}'

        for route in self.routes:
            # Check if route is in list of routes
            match = route.match(path)

            if match:
                # Get identifiers
                identifiers = match.groups()
                action      = self.routes[route]

                return action(identifiers)

        # No route found
        return self.default_route()

router = Router()

from .controllers.overview import OverviewController
