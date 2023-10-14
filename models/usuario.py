from sql_alchemy import banco


class UsuarioModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    nome = banco.Column(banco.String(40))
    tipo = banco.Column(banco.Integer)

    def __init__(self, login, senha, nome, tipo):
        self.login = login
        self.senha = senha
        self.nome = nome
        self.tipo = tipo

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'nome': self.nome,
            'tipo': self.tipo
            }
     
    @classmethod
    def pesquisa_usuario(cls, user_id):
        usuario = cls.query.filter_by(user_id=user_id).first()
        if usuario:
            return usuario
        return None
    
    @classmethod
    def pesquisa_login(cls, login):
        login = cls.query.filter_by(login=login).first()
        if login:
            return login
        return None
    
    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()
        
    def update_usuario(self, nome, login, senha,tipo):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.tipo = tipo
    
    def delete_usuario(self):
        banco.session.delete(self)
        banco.session.commit()
        