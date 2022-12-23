#! python3
# -*- encoding: utf-8 -*-

# from flask import send_file
from app.views.index import index


@index.route('/', methods=['GET'])
def index():
    # return send_file('index.html')
    return "ok"
