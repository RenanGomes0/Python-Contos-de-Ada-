from flask_restful import Resource, reqparse
from models.item import ItemModel
from flask_jwt_extended import jwt_required

        
class Item(Resource):
    def get(self):
        return {'produtos': [Item.json() for Item in ItemModel.query.all()]} 
    

class Atributo(Resource):
    argumentos = reqparse.RequestParser()   
    argumentos.add_argument('titulo', type=str, required=True, help="O Produto tem que ter um titulo")
    argumentos.add_argument('autor',type=str, required=True, help="O Produto tem que ter um autor")
    argumentos.add_argument('categoria',type=str, required=True, help="O Produto tem que ter uma categoria")
    argumentos.add_argument('preco',type=float, required=True, help="O Produto tem que ter um preço")
    argumentos.add_argument('descricao',type=str, required=True,help = "O Produto tem que ter uma descrição")    
    argumentos.add_argument('status',type=int, required=False)
    argumentos.add_argument('id_vendedor',type=int, required=False)       
   
    def get(self, id):
        item = ItemModel.pesquisa(id)
        if item:
            return item.json()        
        return {'message':'cadeee???'} , 404 #not found     
    
    
    class Registro(Resource):
        @jwt_required()
        def post(self):                  
            dados = Atributo.argumentos.parse_args()
            item = ItemModel(**dados)
            try:
                item.save_item()
            except:
                return{'massage':'houve um erro ao salvar'}, 500
            return item.json()
        
       
    @jwt_required()
    def put(self, id):       
        dados = Atributo.argumentos.parse_args()
        item_encontrado = ItemModel.pesquisa(id)
        if item_encontrado:
            item_encontrado.update_item(**dados)
            item_encontrado.save_item()
            return item_encontrado.json(), 200
        item = ItemModel(id, **dados)        
        try:
            item.save_item()
        except:
            return{'massage':'houve um erro ao salvar'}, 500
        return item.json(), 201 
    
    @jwt_required()
    def delete(self, id):
        item = ItemModel.pesquisa(id)
        if item:
            try:
                item.delete_item()
            except:
                return{'massage':'não foi possivel deletar'},500 
            return {'message':'produto deletado'}
        return{'message':'produto não existe'},404