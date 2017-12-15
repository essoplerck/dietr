import re

from ..router import router
from ..models.overview import OverviewModel

class OverviewController:
    def __init__(self):
        self.model = OverviewModel()

    def view(identifiers):
        return 'Hello world!'

router.register_route(r'^/$', OverviewController.view)
