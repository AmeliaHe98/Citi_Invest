from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.expense import ExpenseModel


class Expense(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every expense needs a store_id."
                        )

    @jwt_required()
    def get(self, name):
        expense = ExpenseModel.find_by_name(name)
        if expense:
            return expense.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ExpenseModel.find_by_name(name):
            return {'message': "An expense with name '{}' already exists.".format(name)}, 400

        data = Expense.parser.parse_args()

        expense = ExpenseModel(name, **data)

        try:
            expense.save_to_db()
        except:
            return {"message": "An error occurred inserting the expense."}, 500

        return expense.json(), 201

    def delete(self, name):
        expense = ExpenseModel.find_by_name(name)
        if expense:
            expense.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Expense.parser.parse_args()

        expense = ExpenseModel.find_by_name(name)

        if expense:
            expense.price = data['price']
        else:
            expense = ExpenseModel(name, **data)

        expense.save_to_db()

        return expense.json()


class ExpenseList(Resource):
    def get(self):
        return {'expenses': list(map(lambda x: x.json(), ExpenseModel.query.all()))}