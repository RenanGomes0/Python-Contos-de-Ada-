from flask_restful import Resource, reqparse
from models.livro import LivroModel
from flask_jwt_extended import jwt_required

class Livros(Resource):
    def get(self):
        return {'livros': [livro.json() for livro in LivroModel.query.all()]} 
    

class Atributo(Resource):
    argumentos = reqparse.RequestParser()   
    argumentos.add_argument('titulo', type=str, required=True, help="O livro tem que ter um titulo")
    argumentos.add_argument('autor',type=str, required=True, help="O livro tem que ter um autor")
    argumentos.add_argument('editora',type=str, required=True, help="O livro tem que ter uma editora")
    argumentos.add_argument('preco',type=float, required=True, help="O livro tem que ter um preço")

    
    def get(self, id):
        livro = LivroModel.pesquisa(id)
        if livro:
            return livro.json()        
        return {'message':'cadeee???'} , 404 #not found     
    
    @jwt_required()
    def post(self, id):
        if  LivroModel.pesquisa(id) :
            return {"mesage":"O livro com o id "'{}'" Já existe cabeção".format(id)}, 400
        
        dados = Atributo.argumentos.parse_args()
        livro = LivroModel(id, **dados)
        try:
            livro.save_livro()
        except:
            return{'massage':'houve um erro ao salvar'}, 500
        return livro.json()
       
       
    @jwt_required()
    def put(self, id):       
        dados = Atributo.argumentos.parse_args()
        livro_encontrado = LivroModel.pesquisa(id)
        if livro_encontrado:
            livro_encontrado.update_livro(**dados)
            livro_encontrado.save_livro()
            return livro_encontrado.json(), 200
        livro = LivroModel(id, **dados)        
        try:
            livro.save_livro()
        except:
            return{'massage':'houve um erro ao salvar'}, 500
        return livro.json(), 201 
    
    @jwt_required()
    def delete(self, id):
        livro = LivroModel.pesquisa(id)
        if livro:
            try:
                livro.delete_livro()
            except:
                return{'massage':'não foi possivel deletar'},500 
            return {'message':'livro deletado'}
        return{'message':'livro não existe'},404