from flask_restful import Resource, reqparse
from models.transactions import TransactionsModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.item import ItemModel


class Atributo(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('item_id', type=int, required=True, help="")
    argumentos.add_argument('valor', type=str, required=True, help="")
    argumentos.add_argument('id_comprador', type=int, required=False)


class Transactions(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('item_id', type=int, required=True, help='Item ID é obrigatório')

    class Registro(Resource):
        @jwt_required()
        def post(self):
            user_id = get_jwt_identity()
            dados = Atributo.argumentos.parse_args()

            vendedor_id = ItemModel.pesquisa_vendedor(dados['item_id'])
            dados['id_comprador'] = user_id
            dados['id_vendedor'] = vendedor_id
            dados['item_id'] = dados['item_id']  

            
            transaction = TransactionsModel(**dados)
            
            try:
                transaction.save_transaction()
                return transaction.json(), 201
            except Exception as e:
                return {'message': f'Houve um erro ao salvar: {str(e)}'}, 500
