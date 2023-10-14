from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from secrets import compare_digest
from BLACKLIST import BLACKLIST

atributos = reqparse.RequestParser()     
atributos.add_argument('login', type=str, required=True, help="Tem que ter um login")
atributos.add_argument('senha', type=str, required=True, help="Tem que ter uma senha")

   

class Usuario(Resource):
    def get(self):
        return {'usuarios': [usuario.json() for usuario in UsuarioModel.query.all()]} 
    
#/usuarios/{user_id}
   
    def get(self, user_id):
        usuario = UsuarioModel.pesquisa_usuario(user_id)
        if usuario:
            return usuario.json()        
        return {'message':'cadeee???'} , 404 #not found       

   
    @jwt_required()
    def delete(self, user_id):
        usuario = UsuarioModel.pesquisa_usuario(user_id)
        if usuario:
            try:
                usuario.delete_usuario()
            except:
                return{'massage':'não foi possivel deletar'},500 
            return {'message':'usuario deletado'}
        return{'message':'O usuario não existe'},404
    
    @jwt_required() 
    def put(self, user_id):       
        dados = Usuario.argumentos.parse_args()        
        usuario_encontrado = UsuarioModel.pesquisa_usuario(user_id)
        if usuario_encontrado:
                usuario_encontrado.update_usuario(**dados)
                usuario_encontrado.save_usuario()
        return usuario_encontrado.json(), 200
     
#/cadastro
class RegistroUsuario(Resource):
    def post(self):
          
        dados = atributos.parse_args()
        atributos.add_argument('nome', type=str, required=True, help="Tem que ter um nome")
        atributos.add_argument('tipo', type=int, required=True, help="Tem que ter um tipo")
        
        if UsuarioModel.pesquisa_login(dados['login']):
            return {'message':'Login já em uso'}
        
        usuario = UsuarioModel(**dados)
        usuario.save_usuario()
        return {'mesage':"usuario criado"},201
       
       
#login  de usuario
class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        
        usuario = UsuarioModel.pesquisa_login(dados['login'])
        
        if usuario and compare_digest(usuario.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=usuario.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect.'}, 401

#Logout de usuario

class UserLogout (Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully.'}, 200
 
    
    