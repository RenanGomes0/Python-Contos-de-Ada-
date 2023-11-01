from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from secrets import compare_digest
from BLACKLIST import BLACKLIST
from resources.hash_password import hash_password, check_hashed_password


atributos = reqparse.RequestParser()     
atributos.add_argument('nome', type=str, required=True, help="Tem que ter um nome")
atributos.add_argument('senha', type=str, required=True, help="Tem que ter uma senha")
atributos.add_argument('tipo', type=int, required=True, help="Tem que ter um tipo")
   

class Usuario(Resource):
    def get(self):
        return {'usuarios': [usuario.json() for usuario in UsuarioModel.query.all()]} 
    
#/users/{user_id}
   
    def get(self, user_id):
        usuario = UsuarioModel.pesquisa_usuario(user_id)
        if usuario:
            return usuario.json()        
        return {'message':'cadeee???'} , 404 #not found       

# Mudança nos usuarios
   
    @jwt_required()
    def delete(self, user_id):
        usuario = UsuarioModel.pesquisa_usuario(user_id)
        jwt = get_jwt()
        if jwt.get("tipo") !=1:
            return{"message":"O usuario não é administrador."}
        try:
            usuario.delete_usuario()
        except:
            return{'massage':'não foi possivel deletar'},500 
        return {'message':'usuario deletado'}
            
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
        
        atributos.add_argument('email', type=str, nullable=False, help="Tem que ter um email")
        atributos.add_argument('status', type=int, required=False, default=1)
       
          
        dados = atributos.parse_args()       
        if (len(dados['senha'])) < 8:
            return {"message": "The password length must be at least 8 digits."}
        dados['senha'] = hash_password(dados['senha'])       
        
        if UsuarioModel.pesquisa_nome(dados['nome']):
            return {'message':'Nome já em uso'}
            
        usuario = UsuarioModel(**dados)
        usuario.save_usuario()
        return {'message':"usuario criado"},201
        
#login  de usuario
class UserLogin(Resource):    
    @classmethod
    def post(cls):
        dados = atributos.parse_args()        
        usuario = UsuarioModel.pesquisa_nome(dados['nome']) 
        claims = {"tipo":usuario.tipo,"user_id": usuario.user_id}    
        if usuario and check_hashed_password(dados['senha'], usuario.senha): 
            access_token = create_access_token(identity = usuario.user_id,additional_claims=claims)
            return {'access_token': access_token}, 200
        return{'message': 'Senha ou usuario incorretos.'}, 401

#Logout de usuario

class UserLogout (Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully.'}, 200
 
    
  #ADMIN
  
class AdminLogin(Resource):    
    @classmethod
    def post(cls):
        dados = atributos.parse_args()        
        usuario = UsuarioModel.pesquisa_nome(dados['nome']) 
        claims = {"tipo":usuario.tipo,"user_id": usuario.user_id}    
        if usuario and check_hashed_password(dados['senha'], usuario.senha): 
            access_token = create_access_token(identity = usuario.user_id,additional_claims=claims)
            return {'access_token': access_token}, 200
        return{'message': 'Senha ou usuario incorretos.'}, 401
        