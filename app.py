from flask import Flask, render_template
from flask_restful import Resource, Api
import config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT

from expense import ExpenseList
from income import IncomeList
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
api = Api(app)
app.secret_key = "sprint4"
jwt = JWT(app, authenticate, identity)

api.add_resource(IncomeList, '/income')
api.add_resource(ExpenseList, '/expenses')
api.add_resource(UserRegister, '/login')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/')
def login():
    return render_template('signin.html')
@app.route('/expense/')
def expense():
    return render_template('expenses.html')
@app.route('/income/')
def income():
    return render_template('income.html')
if __name__ == '__main__':
    app.run()
