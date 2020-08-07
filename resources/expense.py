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


class ItemList(Resource):
    def get(self):
        return {'expenses': list(map(lambda x: x.json(), ExpenseModel.query.all()))}
# from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
# import sqlite3
#
#
# class Expense(Resource):
#     TABLE_NAME = 'expenses'
#
#     parser = reqparse.RequestParser()
#     parser.add_argument('price',
#                         type=float,
#                         required=True,
#                         help="This field cannot be left blank!"
#                         )
#
#     @jwt_required()
#     def get(self, name):
#         expense = self.find_by_name(name)
#         if expense:
#             return expense
#         return {'message': 'Item not found'}, 404
#
#     @classmethod
#     def find_by_name(cls, name):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#
#         query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
#         result = cursor.execute(query, (name,))
#         row = result.fetchone()
#         connection.close()
#
#         if row:
#             return {'expense': {'name': row[0], 'price': row[1]}}
#
#     def post(self, name):
#         if self.find_by_name(name):
#             return {'message': "An expense with name '{}' already exists.".format(name)}
#
#         data = Expense.parser.parse_args()
#
#         expense = {'name': name, 'price': data['price']}
#
#         try:
#             Expense.insert(expense)
#         except:
#             return {"message": "An error occurred inserting the expense."}
#
#         return expense
#
#     @classmethod
#     def insert(cls, expense):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#
#         query = "INSERT INTO {table} VALUES(?, ?)".format(table=cls.TABLE_NAME)
#         cursor.execute(query, (expense['name'], expense['price']))
#
#         connection.commit()
#         connection.close()
#
#     @jwt_required()
#     def delete(self, name):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#
#         query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
#         cursor.execute(query, (name,))
#
#         connection.commit()
#         connection.close()
#
#         return {'message': 'Item deleted'}
#
#     @jwt_required()
#     def put(self, name):
#         data = Expense.parser.parse_args()
#         expense = self.find_by_name(name)
#         updated_expense = {'name': name, 'price': data['price']}
#         if expense is None:
#             try:
#                 Expense.insert(updated_expense)
#             except:
#                 return {"message": "An error occurred inserting the expense."}
#         else:
#             try:
#                 Expense.update(updated_expense)
#             except:
#                 return {"message": "An error occurred updating the expense."}
#         return updated_expense
#
#     @classmethod
#     def update(cls, expense):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#
#         query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
#         cursor.execute(query, (expense['price'], expense['name']))
#
#         connection.commit()
#         connection.close()
#
#
# class ExpenseList(Resource):
#     TABLE_NAME = 'expenses'
#
#     def get(self):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#
#         query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
#         result = cursor.execute(query)
#         expenses = []
#         for row in result:
#             expenses.append({'name': row[0], 'price': row[1]})
#         connection.close()
#
#         return {'expenses': expenses}
