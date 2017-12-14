from . import app

class Router:
    def __init__(self):
        self.routes = {}

        @app.route('/')
        @app.route('/<path:path>')
        def __resolve_route(path = ''):
            return self.resolve_route('/' + path)

    def register_route(self, url, action):
        pass

    def default_route(self, *args, **kwargs):
        pass

    def resolve_route(self, path):
        # print url
        print(path)

        return path

router = Router()
