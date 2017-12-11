from . import app
from .controllers.ingredient import IngredientController
from .controllers.session import SessionController


class Router:
    # TODO create a dynamic router
    '''
    The router class is used to encapsulate the routing methods to prevent
    pollution of global namespace.
    '''

    routes = {}

    def __init__(self):
        pass

        @app.route('/')
        @app.route('/<path:path>')
        def __resolve_route(path = ''):
            return self.resolve_route('/{}'.format(path))

    def register_route(self, url, action):
        pass

    def default_route(self, *args, **kwargs):
        pass

    def resolve_route(self, path):
        # print url
        print(path)

        return path

router = Router()
