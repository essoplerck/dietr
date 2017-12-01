class IngredientModel:
    '''
    The ingredient model. This class is used to communicate with the database to
    extract end update data using the CRUD principle. Data may be exchaned using
    a intermediate object.
    '''
    def add_ingredient(self):
        pass

    def edit_ingredient(self):
        pass

    def delete_ingredient(self):
        pass

    def get_ingredient(self, id):
        # Return an example object
        ingredient = {
            'id': id,
            'name': 'Soy Sauce',
            'description': 'Widely used in cooking and as condiment.',
            'allergens': [
                {
                    'id': 1,
                    'name': 'soy beans'
                }, {
                    'id': 2,
                    'name': 'wheat'
                }
            ]
        }

        return ingredient
