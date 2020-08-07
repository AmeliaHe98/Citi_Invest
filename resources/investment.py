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


class InvestmentList(Resource):
    def get(self):
        return {'investments': list(map(lambda x: x.json(), InvestmentModel.query.all()))}
