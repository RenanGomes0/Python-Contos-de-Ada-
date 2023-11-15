from sql_alchemy import banco
from datetime import datetime

class ItemModel(banco.Model):
    __tablename__ = 'items'
    
    id = banco.Column(banco.Integer, primary_key=True)
    titulo = banco.Column(banco.String(80))
    autor = banco.Column(banco.String(80))
    categoria = banco.Column(banco.String(80))
    preco = banco.Column(banco.Float(precision=2))
    descricao = banco.Column(banco.String(120))
    status = banco.Column(banco.Integer)    
    id_vendedor = banco.Column(banco.Integer)
    createdIn = banco.Column(banco.String(30))
    deleted_at = banco.Column(banco.String, default=None, nullable=True)
   
   
    def __init__(self, titulo, autor, categoria, preco, descricao, status, id_vendedor): 
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.preco = preco
        self.descricao = descricao
        self.status = status
        self.id_vendedor = id_vendedor
        self.createdIn = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def json(self):
        return{
            'id' : self.id,
            'titulo' : self.titulo,
            'autor' : self.autor,
            'categoria' : self.categoria,
            'preco' : self.preco,
            'descricao' : self.descricao,
            'status' : self.status,
            'id_vendedor' : self.id_vendedor
            
        }
     
    @classmethod
    def pesquisa(cls, id):
        item = cls.query.filter_by(id=id).first()
        if item:
            return item
        return None
    
    def save_item(self):
        banco.session.add(self)
        banco.session.commit()
        
    def update_item(self, titulo, autor, categoria, preco, descricao, status, id_vendedor):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.preco = preco
        self.descricao = descricao
        self.status = status
        self.id_vendedo = id_vendedor
    
    def delete_item(self):           
        self.status = 0 
        self.deleted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try: 
            banco.session.commit()
        except Exception as e:
            raise Exception(str(e))
        