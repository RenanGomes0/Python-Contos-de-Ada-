from sql_alchemy import banco

class ItemModel(banco.Model):
    __tablename__ = 'items'
    
    id = banco.Column(banco.Integer, primary_key=True)
    titulo = banco.Column(banco.String(80))
    autor = banco.Column(banco.String(80))
    categoria = banco.Column(banco.String(80))
    preco = banco.Column(banco.Float(precision=2))
    descricao = banco.Column(banco.String(120))
    status = banco.Column(banco.Integer)
    id_vendedo = banco.Column(banco.Integer)
    
    def __init__(self, titulo, autor, categoria, preco, descricao, status, id_vendedor): 
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.preco = preco
        self.descricao = descricao
        self.status = status
        self.id_vendedor = id_vendedor
    
    
    def json(self):
        return{
            'id' : self.id,
            'titulo' : self.titulo,
            'autor' : self.autor,
            'categoria' : self.categoria,
            'preco' : self.preco,
            'descricao' : self.descricao,
            'status' : self.status,
            'id_vendedor' : self.id_vendedo
            
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
        banco.session.delete(self)
        banco.session.commit()
        
        