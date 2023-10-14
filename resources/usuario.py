from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel

class Usuario(Resource):
    def get(self):
        return {'usuarios': [usuario.json() for usuario in UsuarioModel.query.all()]} 
    
#/usuarios/{user_id}
   
    def get(self, user_id):
        usuario = UsuarioModel.pesquisa_usuario(user_id)
        if usuario:
            return usuario.json()        
        return {'message':'cadeee???'} , 404 #not found       

   

    def delete(self, user_id):
        usuario = UsuarioModel.pesquisa_usuario(user_id)
        if usuario:
            try:
                usuario.delete_usuario()
            except:
                return{'massage':'não foi possivel deletar'},500 
            return {'message':'usuario deletado'}
        return{'message':'O usuario não existe'},404
    
#/cadastro
class RegistroUsuario(Resource):
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help="Tem que ter um login")
        atributos.add_argument('senha', type=str, required=True, help="Tem que ter uma senha")
        atributos.add_argument('nome', type=str, required=True, help="Tem que ter um nome")
        atributos.add_argument('tipo', type=str, required=True, help="Tem que ter um tipo")
   
    
        dados = atributos.parse_args()
        
        if UsuarioModel.pesquisa_login(dados['login']):
            return {'message':'Login já em uso'}
        
        usuario = UsuarioModel(**dados)
        usuario.save_usuario()
        return {'mesage':"usuario criado"},201
       
       

    def put(self, user_id):       
        dados = Usuario.argumentos.parse_args()        
        usuario_encontrado = UsuarioModel.pesquisa(user_id)
        if usuario_encontrado:
           usuario_encontrado.update_usuario(**dados)
           usuario_encontrado.save_usuario()
        return usuario_encontrado.json(), 200
        usuario = UsuarioModel(user_id,**dados)
        usuario.save_usuario()
        return usuario.json(), 201
      
    
    