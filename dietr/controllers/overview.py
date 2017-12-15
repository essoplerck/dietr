import re

from ..router import router
from ..models.overview import OverviewModel

class OverviewController:
    def __init__(self):
        self.model = OverviewModel()

    def view(self, identifiers):
        return 'Hello world!'

controller = OverviewController()

router.register_route(r'^/$', controller.view)
