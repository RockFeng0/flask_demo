from flask import Blueprint

simple = Blueprint('simple', __name__)

from . import views