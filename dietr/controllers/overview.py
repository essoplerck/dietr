from ..router import router
from ..models.overview import OverviewModel

class OverviewController:
    def __init__(self):
        self.model = OverviewModel()

    @router.register_route('/')
    def view(self):
        return 'Hello world!'
