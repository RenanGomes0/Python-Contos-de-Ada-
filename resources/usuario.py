from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from BLACKLIST import BLACKLIST
from resources.hash_password import hash_password, check_hashed_password


class User(Resource):
    @jwt_required()
    def get(self, user_id):
        jwt = get_jwt()
        if jwt.get("user_type") != 0:
            return {"message": "Admin privilege required."},401
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404 #not found
    
   
    @jwt_required()
    def delete(self, user_id):
        jwt = get_jwt()
        if jwt.get("user_type") != 0:
            return {"message": "Admin privilege required."},401
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
               return {'message': 'An internal error ocurred trying to delete user.'}, 500 
            return {'message': 'User deleted.'}
        return{'message':'User not found.'},404    
        

class UserRegister(Resource):
    def post(self):
        atributes = reqparse.RequestParser()
        atributes.add_argument('login', type=str, required=True, help="The field 'login' cannot be null.")       
        atributes.add_argument('password', type=str, required=True, help="The field 'password' cannot be null.")
        atributes.add_argument('email', type=str, nullable=False, help="Tem que ter um email")
        atributes.add_argument('status', type=int, required=False, default=1)
        atributes.add_argument('type', type=str, required=True, help="The field 'type' cannot be null.")
        dados = atributes.parse_args()
        if (len(dados['password'])) < 8:
            return {"message": "The password length must be at least 8 digits."}
        dados['password'] = hash_password(dados['password'])
        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}, 400
        user = UserModel(**dados)
        user.save_user()
        return {'message':'User created successfully.'}, 201
    
class UpdateUser(Resource):  
    @jwt_required()
    def patch(self):
        jwt = get_jwt()
        if jwt.get("user_type") != 0:
            atributes = reqparse.RequestParser()
            atributes.add_argument('login', type=str)     
            atributes.add_argument('password', type=str)  
            atributes.add_argument('new_password', type=str)
            atributes.add_argument('confirm_password',type=str)
            dados = atributes.parse_args()
            user = UserModel.find_user(jwt.get("user_id"))
        
        if jwt.get("user_type") != 0:
            return {"message": "Admin privilege required."},401
        if dados['login']:
            if (dados["login"] != jwt.get("login") and UserModel.find_by_login(dados['login']) is not None): 
                return {"message": "The login '{}' already exists.".format(dados['login'])}, 400
            else:
                user.login = dados['login']
        if (dados['new_password']!=dados['confirm_password'] or \
        ((dados['new_password'] is None and dados['confirm_password'] is not None) or \
        (dados['new_password'] is not None and dados['confirm_password'] is None))):
            if (dados["password"]) is None:
                return{'message': "Password is needed to confirm this operation."}
            else:
                return {"message": "The new password confirmation didn't match."}, 400
        elif dados['password'] is not None:
            if check_hashed_password(dados['password'], user.password) == False: 
                return {'message':'Password is not correct.'}, 401
            else:
                if dados['new_password'] is not None:
                    if (len(dados['new_password'])) < 8:
                        return {"message": "The password length must be at least 8 digits."}, 400
                    user.password = hash_password(dados['new_password'])
     
        user.update_user(user)
        user.save_user()
        return {'message':'User updated successfully.'}
            
        
        

class UserLogin(Resource):
    @classmethod
    def post(cls):
        atributes = reqparse.RequestParser()
        atributes.add_argument('login', type=str, required=True, help="The field 'login' cannot be null.")
        atributes.add_argument('password', type=str, required=True, help="The field 'password' cannot be null.")
        dados = atributes.parse_args()
        user = UserModel.find_by_login(dados['login'])
        if(user is None):
            return{'message': 'The user was not found.'}, 404
        claims = {"user_type":user.type,"user_id": user.user_id,"login": user.login}
        if(user.status == 0):
            return{'message': 'User is not active.'}, 401
        if user and check_hashed_password(dados['password'], user.password): 
            access_token = create_access_token(identity = user.user_id,additional_claims=claims)
            return {'access_token': access_token}, 200
        return{'message': 'The username or password is incorrect.'}, 401


class UserLogout (Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully.'}, 200

class PasswordReset(Resource):
    @jwt_required()
    def post():
        pass  #é esperado que seja possível realizar a alteração de senha para usuários autenticados e não autenticados
              #para esse, é necessário inserir user, senha antiga, senha nova e confirmar senha nova. Tambem adicionar 
              # lógica para verificar se é o próprio user que está mudando a senha e/ou se é um admin


#ADM
class AdminLogin(Resource):
    @classmethod
    def post(cls):
        atributes = reqparse.RequestParser()
        atributes.add_argument('login', type=str, required=True, help="The field 'login' cannot be null.")
        atributes.add_argument('password', type=str, required=True, help="The field 'password' cannot be null.")
       
        dados = atributes.parse_args()
        user = UserModel.find_by_login(dados['login'])
        if ("user_type") != 0:
            return {"message": "Admin privilege required."},401
        if(user is None):
            return{'message': 'The user was not found.'}, 404
        claims = {"user_type":user.type,"user_id": user.user_id,"login": user.login}
        if(user.status == 0):
            return{'message': 'User is not active.'}, 401
        if user and check_hashed_password(dados['password'], user.password): 
            access_token = create_access_token(identity = user.user_id,additional_claims=claims)
            return {'access_token': access_token}, 200
        return{'message': 'The username or password is incorrect.'}, 401
