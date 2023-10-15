from sql_alchemy import banco

class UsuarioModel(banco.Model):
    __tablename__ = 'usuarios'
    
    user_id = banco.Column(banco.Integer, primary_key=True)    
    nome = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    email = email.Column(banco.String(80))
    status = status.Column(banco.Integer)
    tipo = banco.Column(banco.String(40))

    def __init__(self,nome, senha, email, status, tipo):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.status = status
        self.tipo = tipo

    def json(self):
        return {
            'user_id': self.user_id,
            'nome': self.nome,
            'email': self.email,
            'tipo': self.tipo,
            'status':self.status
            }
     
    @classmethod
    def pesquisa_usuario(cls, user_id):
        usuario = cls.query.filter_by(user_id=user_id).first()
        if usuario:
            return usuario
        return None
    
    @classmethod
    def pesquisa_nome(cls, nome):
        nome = cls.query.filter_by(nome=nome).first()
        if nome:
            return nome
        return None
    
    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()
        
    def update_usuario(self, nome, senha, email, status, tipo):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.status = status
        self.tipo = tipo
    
    def delete_usuario(self):
        banco.session.delete(self)
        banco.session.commit()
        