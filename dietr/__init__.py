from flask import Blueprint

app = Blueprint('dietr', __name__,
                template_folder = 'templates',
                static_folder   = 'static')
