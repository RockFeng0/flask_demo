#! python3
# -*- encoding: utf-8 -*-


from flask import Blueprint
task = Blueprint('task', __name__)

from . import views
