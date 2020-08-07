from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.income import IncomeModel


class Income(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every income needs a store_id."
                        )

    @jwt_required()
    def get(self, name):
        income = IncomeModel.find_by_name(name)
        if income:
            return income.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if IncomeModel.find_by_name(name):
            return {'message': "An income with name '{}' already exists.".format(name)}, 400

        data = Income.parser.parse_args()

        income = Income(name, **data)

        try:
            income.save_to_db()
        except:
            return {"message": "An error occurred inserting the income."}, 500

        return income.json(), 201

    def delete(self, name):
        income = IncomeModel.find_by_name(name)
        if income:
            income.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Income.parser.parse_args()

        income = IncomeModel.find_by_name(name)

        if income:
            income.price = data['price']
        else:
            income = IncomeModel(name, **data)

        income.save_to_db()

        return income.json()


class IncomeList(Resource):
    def get(self):
        return {'incomes': list(map(lambda x: x.json(), IncomeModel.query.all()))}
# from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
# import sqlite3
#
#
# class Income(Resource):
#     TABLE_NAME = 'income'
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
#         income = self.find_by_name(name)
#         if income:
#             return income
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
#             return {'income': {'name': row[0], 'price': row[1]}}
#
#     def post(self, name):
#         if self.find_by_name(name):
#             return {'message': "An income with name '{}' already exists.".format(name)}
#
#         data = Income.parser.parse_args()
#
#         income = {'name': name, 'price': data['price']}
#
#         try:
#             Income.insert(income)
#         except:
#             return {"message": "An error occurred inserting the income."}
#
#         return income
#
#     @classmethod
#     def insert(cls, income):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#
#         query = "INSERT INTO {table} VALUES(?, ?)".format(table=cls.TABLE_NAME)
#         cursor.execute(query, (income['name'], income['price']))
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
#         data = Income.parser.parse_args()
#         income = self.find_by_name(name)
#         updated_income = {'name': name, 'price': data['price']}
#         if income is None:
#             try:
#                 Income.insert(updated_income)
#             except:
#                 return {"message": "An error occurred inserting the income."}
#         else:
#             try:
#                 Income.update(updated_income)
#             except:
#                 return {"message": "An error occurred updating the income."}
#         return updated_income
#
#     @classmethod
#     def update(cls, income):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#
#         query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
#         cursor.execute(query, (income['price'], income['name']))
#
#         connection.commit()
#         connection.close()
#
#
# class IncomeList(Resource):
#     TABLE_NAME = 'income'
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
