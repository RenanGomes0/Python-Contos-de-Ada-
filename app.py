from flask import Flask   
from flask_restful import  Api
from resources.livro import Livros, Atributo
from resources.usuario import Usuario, RegistroUsuario, UserLogin
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyonne'
api = Api(app)
jwt = JWTManager(app)

@app.before_request
def cria_banco():
    banco.create_all()    

api.add_resource(Livros,'/livros')     
api.add_resource(Atributo,'/livros/<int:id>')
api.add_resource(Usuario,'/usuarios/<int:user_id>')
api.add_resource(RegistroUsuario,'/cadastro')
api.add_resource(UserLogin,'/login')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
