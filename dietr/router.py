from . import app

class Router:
    def __init__(self):
        self.routes = {}

        @app.route('/')
        @app.route('/<path:path>')
        def __resolve_route(path = ''):
            return self.resolve_route('/' + path)

    def register_route(self, url, action, methods = ['GET', 'POST']):
        action.methods = methods

        self.routes[url] = action

    def default_route(self, *args, **kwargs):
        pass

    def resolve_route(self, path):
        # Check if route is in list of routes
        if path in self.routes:
            return self.routes[path]()

        else:
            return self.default_route()

router = Router()
