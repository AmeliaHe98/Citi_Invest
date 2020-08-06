from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
# from flask import Flask, render_template
# from flask_restful import Api
# from flask_jwt import JWT
# from expense import ExpenseList
# from income import IncomeList
# from security import authenticate, identity
# from resources.user import UserRegister
#
# app = Flask(__name__)
# api = Api(app)
# app.secret_key = "sprint4"
# jwt = JWT(app, authenticate, identity)
#
# api.add_resource(IncomeList, '/income')
# api.add_resource(ExpenseList, '/expenses')
# api.add_resource(UserRegister, '/login')
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/login/')
# def login():
#     return render_template('sign-in.html')
#
# if __name__ == '__main__':
#     app.run()
