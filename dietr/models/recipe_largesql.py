def get_recipe(self, allergy_tuple, start, limit):

    query = '''SELECT recipes.id,
        		recipes.name,
                recipes.url,
        		images.url AS image,
                extra_info.name AS extra

                FROM recipes

                INNER JOIN images
                ON recipes.image_id = images.id

                INNER JOIN recipes_extra_info
                ON recipes_extra_info.recipe_id = recipes.id

                INNER JOIN extra_info
                ON extra_info.id = recipes_extra_info.extra_info_id

                INNER JOIN recipes_ingredients
                ON recipes_ingredients.recipe_id = recipes.id

                INNER JOIN allergies_ingredients
                ON allergies_ingredients.ingredient_id = recipes_ingredients.ingredient_id

                WHERE recipes.id NOT IN
                (SELECT recipe_id FROM recipes_ingredients
                 WHERE allergies_ingredients.allergy_id IN %s)

                GROUP BY recipes.id

                LIMIT %s, %s'''

    recipes = database.fetch_all(query, (allergy_tuple, start, limit))

    return [Recipe(**recipe) for recipe in recipes]


def get_recipe_count(self, allergy_tuple):

    if not allergy_tuple:
        query = '''SELECT COUNT(*) FROM recipes'''
        count = database.fetch(query)

    else:
        query = '''SELECT COUNT(*)
                            FROM (SELECT recipe_id FROM recipes_ingredients

                            INNER JOIN allergies_ingredients
                            ON allergies_ingredients.ingredient_id = recipes_ingredients.ingredient_id

                            WHERE allergies_ingredients.allergy_id NOT IN %s
                            GROUP BY recipe_id) A'''

        count = database.fetch(query, (allergy_tuple,))

    return count['COUNT(*)']
