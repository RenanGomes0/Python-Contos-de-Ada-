from flask import Flask, jsonify   
from flask_restful import  Api
from resources.item import Item, Atributo
from resources.usuario import User, UserRegister, UserLogin, UserLogout, AdminLogin,UpdateUser,UpdateUserAdmin,Users
from flask_jwt_extended import JWTManager
from BLACKLIST import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyonne'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_request
def cria_banco():
    banco.create_all()    

@jwt.token_in_blocklist_loader
def verificablacklist(self,token):
    return token ['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify ({'message':'Você esta deslogado'})
#itens    
api.add_resource(Item,'/itens')
api.add_resource(Atributo.Registro,'/itens')     
api.add_resource(Atributo.Update,'/itens/<int:id>')
api.add_resource(Atributo.DeleteId,'/itens/<int:id>')
api.add_resource(Atributo.DeleteCategoria, '/itens/categoria/<string:categoria>')


#Usuario
api.add_resource(UserRegister,'/users/signup')
api.add_resource(UserLogin,'/users/login')
api.add_resource(UserLogout,'/logout')
api.add_resource(UpdateUser,'/users/<int:user_id>')
#ADM
api.add_resource(User,'/admin/users/<int:user_id>')
api.add_resource(Users,'/admin/users')
api.add_resource(AdminLogin,'/admin/login')
api.add_resource(UpdateUserAdmin,'/admin/users/<int:user_id>')



if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
