from flask import Flask
from functools import wraps
from flaskext.mysql import MySQL
from flask import render_template
from flask import request

from diet_person_model import *
from diet_ingredient_model import *
from diet_category_model import *
from connection import *

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

def get_session_account_id():#Todo
    return 1

ingredient_model = DietIngredientModel()
category_model = DietCategoryModel()
person_model = DietPersonModel()

@app.route('/request_search_ingredient/<search_word>')
def request_search_ingredient(search_word):
    return ingredient_model.request_search_ingredient(search_word);

@app.route('/request_search_category/<search_word>')
def request_search_category(search_word):
    return category_model.request_search_category(search_word);

@app.route('/update_diet_category/<person_name>/<category_id>')#Both used for adding and deleting an category to a diet (destroyed when exists added when not exists)
def update_diet_category(person_name, category_id):
    account_id = get_session_account_id()
    person_id = person_model.find_person_id(account_id, person_name)
    if(person_id!=-1):
        category_model.post_category(person_id, category_id)
        return str(person_id)
    return ""
    
@app.route('/update_diet_ingredient/<person_name>/<ingredient_id>')#Both used for adding and deleting an ingredient to a diet (destroyed when exists added when not exists)
def update_diet_ingredient(person_name, ingredient_id):
    account_id = get_session_account_id()
    person_id = person_model.find_person_id(account_id, person_name)
    if(person_id!=-1):
        ingredient_model.post_ingredient(person_id, ingredient_id)
        return str(person_id)
    return ""
    
@app.route('/diet', methods=['GET', 'POST'])
def diet_zonder():
    account_id = get_session_account_id()
    person_list = person_model.render_person_list(account_id)
    ingredient_list = ingredient_model.render_current_ingredient_list(account_id);
    category_list = category_model.render_current_category_list(account_id)

    return render_template('diet/select.html', ingredient_list=ingredient_list, category_list=category_list, person_list=person_list)

@app.route('/diet/<person_name>', methods=['GET', 'POST'])
def diet_person(person_name):
    account_id = get_session_account_id()
    person_list = person_model.render_person_list(account_id)
    ingredient_list = ingredient_model.render_current_ingredient_list(account_id);
    category_list = category_model.render_current_category_list(account_id)

    return render_template('diet/select.html', ingredient_list=ingredient_list, category_list=category_list, person_list=person_list)
    
@app.route('/diet/<person_name>/<search_word>', methods=['GET', 'POST'])
def diet(person_name, search_word):
    account_id = get_session_account_id()
    person_list = person_model.render_person_list(account_id)
    ingredient_list = ingredient_model.render_current_ingredient_list(person_model.find_person_id(account_id, person_name))
    category_list = category_model.render_current_category_list(person_model.find_person_id(account_id, person_name))

    return render_template('diet/select.html', ingredient_list=ingredient_list, category_list=category_list, person_list=person_list)