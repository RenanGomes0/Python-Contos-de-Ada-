from flask import Flask   
from flask_restful import  Api
from resources.livro import Livros, Atributo
from resources.usuario import Usuario,RegistroUsuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

app._got_first_request
def cria_banco():
    banco.create_all()    

api.add_resource(Livros,'/livros')     
api.add_resource(Atributo,'/livros/<int:id>')
api.add_resource(Usuario,'/usuarios/<int:user_id>')
api.add_resource(RegistroUsuario,'/cadastro')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
