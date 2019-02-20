from flask import Blueprint

sql = Blueprint('sql', __name__)
from . import views
