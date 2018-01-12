#Het diet_category_model zorgt ervoor dat de allergiën in een persoons dieet worden opgehaald en aangepast kunnen worden
from connection import *

class DietCategoryModel:
    def check_if_category_in_diet(self, person_id, category_id):
        query="select * from person_category_relation where person_id=%s and category_id=%s;"
        data=(person_id, category_id)
        
        cursor=connection.cursor()
        if cursor.execute(query, data)>0:
            userdata=cursor.fetchone()
                
            cursor.close()
            return True
            
        cursor.close()
        return False

    def post_category(self, person_id, category_id):
        if self.check_if_category_in_diet(person_id, category_id):
            self.remove_category_from_diet(person_id, category_id)
        else:
            self.add_category_to_diet(person_id, category_id)

    def add_category_to_diet(self, person_id, category_id):
        query="insert into person_category_relation (person_id, category_id) values (%s, %s);"
        data=(person_id, category_id)
        
        cursor=connection.cursor()
        cursor.execute(query, data)
        connection.commit()
            
        cursor.close()
        return category_id;

    def remove_category_from_diet(self, person_id, category_id):
        query="delete from person_category_relation where person_id=%s and category_id=%s;"
        data=(person_id, category_id)
        
        cursor=connection.cursor()
        cursor.execute(query, data)
        connection.commit()
            
        cursor.close()
        
    def render_current_category_list(self, person_id):#Displays the users current ingredient in diet list. The output is a string an is formated like x|y|x|y where x is the category_id and y the category_name
        if(person_id!=-1):
            query="select * from person_category_relation left join category on category.id=person_category_relation.category_id and person_category_relation.person_id=%s;"
            data=(person_id)
            
            cursor=connection.cursor()
            cursor.execute(query, data)
            row=cursor.fetchone()
            output=""
            first_row=True
            while row is not None:
                category_id=row["category.id"]
                category_name=row["name"]
                if(category_name is not None):
                    if(first_row):
                        first_row=False
                    else:
                        output+="|"
                    output+=str(category_id)+"|"+str(category_name)
                row=cursor.fetchone()
                
            cursor.close()
            return output
        else:
            return "";

    def request_search_category(self, search_word):#Executed when the user types in the add to diet search box. The output is a string an is formated like x|y|x|y where x is the category_id and y the category_name
        query="select * from category where locate(%s, category.name) > 0 and not exists (select * from person_category_relation where category.id = person_category_relation.category_id);"
        data=(search_word)
        cursor=connection.cursor()
        cursor.execute(query, data)
        row=cursor.fetchone()
        output=""
        first_row=True
        while row is not None:
            category_id=row["id"]
            category_name=row["name"]
            if(first_row):
                first_row=False
            else:
                output+="|"
            output+=str(category_id)+"|"+category_name
            row=cursor.fetchone()
        cursor.close()
        return output