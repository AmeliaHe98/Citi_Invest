from db import db


class IncomeModel(db.Model):
    __tablename__ = 'incomes'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    amount = db.Column(db.Float(precision=2))

    username = db.Column(db.String(80), db.ForeignKey('users.username'))
    user = db.relationship('UserModel')

    def __init__(self, type, amount, username):
        self.type = type
        self.amount = amount
        self.username = username

    def json(self):
        return {'type': self.type, 'amount': self.amount}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()