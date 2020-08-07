from db import db


class ExpenseModel(db.Model):
    __tablename__ = 'expenses'

    transaction_id = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String(80))
    amount = db.Column(db.Float(precision=2))
    payment_type = db.Column(db.String(80))
    #datetime = db.Column(db.DateTime)

    username = db.Column(db.String(80), db.ForeignKey('users.username'))
    user = db.relationship('UserModel')

    def __init__(self, Category, amount, username, payment_type):
        self.Category = Category
        self.amount = amount
        self.username = username
        self.payment_type = payment_type

    def json(self):
        return {'Category': self.Category, 'Amount': self.amount, }

    @classmethod
    def find_by_name(cls, Category):
        return cls.query.filter_by(Category=Category).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()