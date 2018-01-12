#Het diet_ingrediet_model zorgt ervoor dat de ongewensde ingredienten in een persoons dieet worden opgehaald en aangepast kunnen worden
from connection import *

class DietIngredientModel:
    def check_if_ingredient_in_diet(self, person_id, ingredient_id):
        query="select * from person_ingredient_relation where person_id=%s and ingredient_id=%s;"
        data=(person_id, ingredient_id)
        
        cursor=connection.cursor()
        if cursor.execute(query, data)>0:
            userdata=cursor.fetchone()
                
            cursor.close()
            return True
            
        cursor.close()
        return False
        
    def post_ingredient(self, person_id, ingredient_id):
        if self.check_if_ingredient_in_diet(person_id, ingredient_id):
            self.remove_ingredient_from_diet(person_id, ingredient_id)
        else:
            self.add_ingredient_to_diet(person_id, ingredient_id)

    def add_ingredient_to_diet(self, person_id, ingredient_id):
        query="insert into person_ingredient_relation (person_id, ingredient_id) values (%s, %s);"
        data=(person_id, ingredient_id)
        
        cursor=connection.cursor()
        cursor.execute(query, data)
        connection.commit()
            
        cursor.close()
        return ingredient_id;

    def remove_ingredient_from_diet(self, person_id, ingredient_id):
        query="delete from person_ingredient_relation where person_id=%s and ingredient_id=%s;"
        data=(person_id, ingredient_id)
        
        cursor=connection.cursor()
        cursor.execute(query, data)
        connection.commit()
            
        cursor.close()

    def render_current_ingredient_list(self, person_id):#Displays the users current ingredient in diet list. The output is a string an is formated like x|y|x|y where x is the ingredient_id and y the ingredient_name
        if(person_id!=-1):
            query="select * from person_ingredient_relation left join ingredient on ingredient.id=person_ingredient_relation.ingredient_id and person_ingredient_relation.person_id=%s;"
            data=(person_id)
            
            cursor=connection.cursor()
            cursor.execute(query, data)
            row=cursor.fetchone()
            output=""
            first_row=True
            while row is not None:
                ingredient_id=row["ingredient.id"]
                ingredient_name=row["name"]
                if(ingredient_name is not None):
                    if(first_row):
                        first_row=False
                    else:
                        output+="|"
                    output+=str(ingredient_id)+"|"+str(ingredient_name)
                row=cursor.fetchone()
                
            cursor.close()
            return output
        else:
            return "";

    def request_search_ingredient(self, search_word):#Executed when the user types in the add to diet search box. The output is a string an is formated like x|y|x|y where x is the ingredient_id and y the ingredient_name
        query="select * from ingredient where locate(%s, ingredient.name) > 0 and not exists (select * from person_ingredient_relation where ingredient.id = person_ingredient_relation.ingredient_id);"
        data=(search_word)
        cursor=connection.cursor()
        cursor.execute(query, data)
        row=cursor.fetchone()
        output=""
        first_row=True
        while row is not None:
            ingredient_id=row["id"]
            ingredient_name=row["name"]
            if(first_row):
                first_row=False
            else:
                output+="|"
            output+=str(ingredient_id)+"|"+ingredient_name
            row=cursor.fetchone()
        cursor.close()
        return output