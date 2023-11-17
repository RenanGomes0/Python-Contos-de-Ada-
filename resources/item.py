from flask_restful import Resource, reqparse
from models.item import ItemModel
from flask_restful import Resource
from models.usuario import UserModel
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
       
class Item(Resource):
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        if jwt.get("user_type") != 0:
            return {"message": "Admin privilege required."}, 401

        user = UserModel.find_user(jwt["user_id"])
        if not user:
            return {"message": "User not found."}, 404

        try:
            # Adicione a condição de status=1 diretamente na consulta
            items = ItemModel.query.filter_by(status=1).all()

            if items:
                return {'produtos': [item.json() for item in items]} 
            return {'message': 'No items found with status 1.'}, 404
        except Exception as e:
            return {'message': f'Houve um erro ao buscar os itens: {str(e)}'}, 500

    
    class Titulo(Resource):
        @jwt_required()
        def get(self, titulo):
            jwt = get_jwt()
            if jwt.get("user_type") != 0:
                return {"message": "Admin privilege required."}, 401
            user = UserModel.find_user(jwt["user_id"])
            if not user:
                return {"message": "User not found."}, 404

            # Modificação para garantir que apenas itens com status diferente de 0 sejam incluídos
            itens = ItemModel.query.filter(ItemModel.titulo.ilike(f"%{titulo}%"), ItemModel.status != 0).all()

            if itens:
                return {'produtos': [item.json() for item in itens]}
            return {'message': 'No items found with the given title and status not equal to 0.'}, 404
 

    class Categoria(Resource):
        @jwt_required()
        def get(self):
            jwt = get_jwt()
            if jwt.get("user_type") != 0:
                return {"message": "Admin privilege required."}, 401
            user = UserModel.find_user(jwt["user_id"])
            if not user:
                return {"message": "User not found."}, 404

            categorias = (
                ItemModel.query
                .filter(ItemModel.status != 0)
                .distinct(ItemModel.categoria)
                .all()
            )

            if categorias:
                return {'categorias': list(set(categoria.categoria for categoria in categorias))}
            return {'message': 'No items found with status not equal to 0.'}, 404

      
    

class Atributo(Resource):
    argumentos = reqparse.RequestParser()   
    argumentos.add_argument('titulo', type=str, required=True, help="O Produto tem que ter um titulo")
    argumentos.add_argument('autor',type=str, required=True, help="O Produto tem que ter um autor")
    argumentos.add_argument('categoria',type=str, required=True, help="O Produto tem que ter uma categoria (livro, jornal, revista ou periodico)")
    argumentos.add_argument('preco',type=float, required=True, help="O Produto tem que ter um preço")
    argumentos.add_argument('descricao',type=str, required=True,help = "O Produto tem que ter uma descrição")    
    argumentos.add_argument('status', type=int, required=False, default=1)
    argumentos.add_argument('id_vendedor',type=int, required=False)       
   
    class Procura(Resource):
        @jwt_required()
        def get(self, id):
            jwt = get_jwt()
            if jwt.get("user_type") != 0:
                return {"message": "Admin privilege required."}, 401

            user = UserModel.find_user(jwt["user_id"])

            if not user:
                return {"message": "User not found."}, 404

            item = ItemModel.pesquisa(id)

            if item:
                return item.json()

            return {'message': 'Item not found.'}, 404
        
    
    class Registro(Resource):
        @jwt_required()
        def post(self):
            user_id = get_jwt_identity()
            dados = Atributo.argumentos.parse_args()
            dados['id_vendedor'] = user_id
            item = ItemModel(**dados)
            try:
                item.save_item()
                return item.json(), 201
            except Exception as e:
                return {'message': f'Houve um erro ao salvar: {str(e)}'}, 500

    class Update(Resource):       
        @jwt_required()
        def put(self, id):
            dados = Atributo.argumentos.parse_args()
            item_encontrado = ItemModel.pesquisa(id)

            if item_encontrado:
                try:
                    item_encontrado.update_item(**dados)
                    item_encontrado.save_item()
                    return item_encontrado.json(), 200
                except Exception as e:
                    return {'message': f'Houve um erro ao atualizar: {str(e)}'}, 500
            else:
                return {'message': 'Item não encontrado'}, 404


            
    class DeleteId(Resource):
        @jwt_required()
        def delete(self, id):
            item = ItemModel.pesquisa(id)
            if item:
                try:
                    item.delete_item()
                    return {'message': 'Produto deletado'}
                except Exception as e:
                    return {'message': f'Não foi possível deletar: {str(e)}'}, 500

            return {'message': 'Produto não existe'}, 404
    
    class DeleteCategoria(Resource):
        @jwt_required()
        def delete(self, categoria):
            itens = ItemModel.pesquisa_por_categoria(categoria)
            if itens:
                try:
                    for item in itens:
                        item.delete_item()
                    return {'message': 'Produtos deletados'}
                except Exception as e:
                    return {'message': f'Não foi possível deletar: {str(e)}'}, 500
            else:
                return {'message': 'Produtos não existem'}, 404
