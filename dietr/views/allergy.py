from flask import Blueprint

blueprint = Blueprint('allergy', __name__)


@blueprint.route('/allergy/add', methods=['GET', 'POST'])
def add():
    pass


@blueprint.route('/allergy/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    pass


@blueprint.route('/allergy/<int:id>/remove', methods=['GET', 'POST'])
def remove(id):
    pass


@blueprint.route('/allergy/<int:id>')
def view(id):
    pass


@blueprint.route('/allergies')
def overview():
    pass
