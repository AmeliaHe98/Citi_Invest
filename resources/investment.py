from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.investment import InvestmentModel


class Investment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every investment needs a store_id."
                        )

    @jwt_required()
    def get(self, name):
        investment = InvestmentModel.find_by_name(name)
        if investment:
            return investment.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if InvestmentModel.find_by_name(name):
            return {'message': "An investment with name '{}' already exists.".format(name)}, 400

        data = Investment.parser.parse_args()

        investment = InvestmentModel(name, **data)

        try:
            investment.save_to_db()
        except:
            return {"message": "An error occurred inserting the investment."}, 500

        return investment.json(), 201

    def delete(self, name):
        investment = InvestmentModel.find_by_name(name)
        if investment:
            investment.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Investment.parser.parse_args()

        investment = InvestmentModel.find_by_name(name)

        if investment:
            investment.price = data['price']
        else:
            investment = InvestmentModel(name, **data)

        investment.save_to_db()

        return investment.json()


class ItemList(Resource):
    def get(self):
        return {'investments': list(map(lambda x: x.json(), InvestmentModel.query.all()))}
# from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
# import sqlite3
#
#
# class Investment(Resource):
#     TABLE_NAME = 'investment'
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
#         investment = self.find_by_name(name)
#         if investment:
#             return investment
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
#             return {'investment': {'name': row[0], 'price': row[1]}}
#
#     def post(self, name):
#         if self.find_by_name(name):
#             return {'message': "An investment with name '{}' already exists.".format(name)}
#
#         data = Investment.parser.parse_args()
#
#         investment = {'name': name, 'price': data['price']}
#
#         try:
#             Investment.insert(investment)
#         except:
#             return {"message": "An error occurred inserting the investment."}
#
#         return investment
#
#     @classmethod
#     def insert(cls, investment):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#
#         query = "INSERT INTO {table} VALUES(?, ?)".format(table=cls.TABLE_NAME)
#         cursor.execute(query, (investment['name'], investment['price']))
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
#         data = Investment.parser.parse_args()
#         investment = self.find_by_name(name)
#         updated_investment = {'name': name, 'price': data['price']}
#         if investment is None:
#             try:
#                 Investment.insert(updated_investment)
#             except:
#                 return {"message": "An error occurred inserting the investment."}
#         else:
#             try:
#                 Investment.update(updated_investment)
#             except:
#                 return {"message": "An error occurred updating the investment."}
#         return updated_investment
#
#     @classmethod
#     def update(cls, investment):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#
#         query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
#         cursor.execute(query, (investment['price'], investment['name']))
#
#         connection.commit()
#         connection.close()
#
#
# class InvestmentList(Resource):
#     TABLE_NAME = 'investment'
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