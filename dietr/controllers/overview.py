from ..router import router
from ..models.overview import OverviewModel

class OverviewController:
    def __init__(self):
        self.model = OverviewModel()

    def view():
        return 'Hello world!'

router.register_route('/test', OverviewController.view)
