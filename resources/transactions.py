from flask_restful import Resource, reqparse
from models.transactions import TransactionsModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.item import ItemModel


class Transactions(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('item_id', type=int, required=True, help='Item ID é obrigatório')

    class Registro_transactions(Resource):
        @jwt_required()
        def post(self):
            user_id = get_jwt_identity()
            dados = Transactions.parser.parse_args()

            item = ItemModel.pesquisar_item_por_id(dados['item_id'])

            if item is None:
                return {'message': 'Item não encontrado para o ID fornecido'}, 404

            dados['comprador_id'] = user_id
            dados['vendedor_id'] = item.id_vendedor
            dados['preco'] = item.preco  

            try:
              
                transaction = TransactionsModel(**dados)
                transaction.save_transaction()
                return transaction.json(), 201
            except Exception as e:
                return {'message': f'Houve um erro ao salvar: {str(e)}'}, 500
