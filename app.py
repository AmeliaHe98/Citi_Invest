from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
# from resources.item import Item, ItemList
# from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/login/')
def login():
    return render_template('sign-in.html')

@app.route('/expenses/')
def expense():
    return render_template('expenses.html')
  
@app.route('/income/')
def income():
    return render_template('income.html')

if __name__ == '__main__':
    app.run(port=8910)
