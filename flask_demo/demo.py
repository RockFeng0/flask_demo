#! python3
# -*- encoding: utf-8 -*-
'''
Current module: flask_demo.demo

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      flask_demo.demo,v 1.0 2019年2月20日
    FROM:   2019年2月20日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import os,sys
from flask_demo.demo import app
 
if __name__ == "__main__":
    os.environ["FLASK_APP"] = 'demo.manager'
    if not os.path.isfile('demo.db'):
        print('----- init')
        os.system("{} -m flask db init".format(sys.executable))
        print('----- migrate')
        os.system("{} -m flask db migrate".format(sys.executable))
        print('----- upgrade')
        os.system("{} -m flask db upgrade".format(sys.executable))
        print('----- done')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{0}".format(os.path.join(os.getcwd(), "demo.db"))
    print('----- {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))
    app.run(host='0.0.0.0', port=5000, debug = True)
    

    
    