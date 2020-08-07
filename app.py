from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.expense import Expense, ExpenseList
from resources.income import Income, IncomeList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
app.secret_key = "sprint4"


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(IncomeList, '/income')
api.add_resource(ExpenseList, '/expenses')
api.add_resource(UserRegister, '/login')

users = [
    {
        'username': 'Ameliahe',
        'password': '9999'
    }
]

expenses = [{
    'amount': 12.14,
    'payment type': "mastercard",
    'category': "grocery"
}]


@app.route('/')
def index():
    request_data = request.get_json()
    new_user = {
        'username': 'linhang',
        'password': '666',
    }
    users.append(new_user)
    # return jsonify(new_user)
    return render_template('index.html')


@app.route('/login/')
def login():
    return render_template('sign-in.html')


@app.route('/income/')
def income():
    return render_template('income.html')

@app.route('/expense/')
def expense():
    return render_template('expenses.html')

db.init_app(app)
