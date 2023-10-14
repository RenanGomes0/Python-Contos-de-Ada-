from sql_alchemy import banco

class LivroModel(banco.Model):
    __tablename__ = 'livros'
    
    id = banco.Column(banco.Integer, primary_key=True)
    titulo = banco.Column(banco.String(80))
    autor = banco.Column(banco.String(80))
    editora = banco.Column(banco.String(80))
    preco = banco.Column(banco.Float(precision=2))
    
    def __init__(self, id, titulo, autor, editora, preco): 
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.preco = preco
    
    
    def json(self):
        return{
            'id' : self.id,
            'titulo' : self.titulo,
            'autor' : self.autor,
            'editora' : self.editora,
            'preco' : self.preco
        }
     
    @classmethod
    def pesquisa(cls, id):
        livro = cls.query.filter_by(id=id).first()
        if livro:
            return livro
        return None
    
    def save_livro(self):
        banco.session.add(self)
        banco.session.commit()
        
    def update_livro(self, titulo, autor, editora, preco):
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.preco = preco
    
    def delete_livro(self):
        banco.session.delete(self)
        banco.session.commit()
        