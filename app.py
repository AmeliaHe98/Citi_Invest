from flask import Flask, render_template
import config

app = Flask(__name__)
app.config.from_object(config)


class Person(object):
    name = ''
    age = 0


class Expense(object):
    pass


class Investment(object):
    pass


class Income(object):
    pass


class Account(object):
    pass


@app.route('/')
def index():
    return render_template('index.html')


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
    app.run(port=5000)
