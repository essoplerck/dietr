#Het diet_person_model zorgt voor het ophalen van de gegevens van de personen van een bepaald account
from connection import *

class DietPersonModel:
    def render_person_list(self, account_id):#Geeft een lijst van alle personen van het gegeven account_id. Geformateerd als een string x|x|x waar x de persoon naam is
        query="select * from person where account_id=%s;"
        data=(account_id)
        cursor=connection.cursor()
        cursor.execute(query, data)
        row=cursor.fetchone()
        output=""
        first_row=True
        while row is not None:
            person_name=row["name"]  
            if(first_row):
                first_row=False
            else:
                output+="|"
            output+=person_name
            row=cursor.fetchone()
        cursor.close()
        return output

    def find_person_id(self, account_id, person_name):
        query="select * from person where account_id=%s and name=%s;"
        data=(account_id, person_name)
        cursor=connection.cursor()
        if cursor.execute(query, data)>0:
            userdata=cursor.fetchone()
            cursor.close()
            return userdata["id"]
        cursor.close()
        return -1