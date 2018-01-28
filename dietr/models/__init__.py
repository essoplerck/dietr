from dietr.models.allergy import AllergyModel
from dietr.models.ingredient import IngredientModel
from dietr.models.pantry import PantryModel
from dietr.models.recipe import RecipeModel
from dietr.models.roommate import RoommateModel
from dietr.models.user import UserModel


class Model:
    allergy = AllergyModel()
    ingredient = IngredientModel()
    pantry = PantryModel()
    recipe = RecipeModel()
    roommate = RoommateModel()
    user = UserModel()


model = Model()
