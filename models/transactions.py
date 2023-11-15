from sql_alchemy import banco
from datetime import datetime


class TransactionsModel(banco.Model):
    __tablename__ = 'transactions'
    
    id = banco.Column(banco.Integer, primary_key=True)
    id_comprador = banco.Column(banco.String(80))
    id_vendor = banco.Column(banco.String(80))
    id_item = banco.Column(banco.String(80))
    preco = banco.Column(banco.Float(precision=2))
    id_vendedor = banco.Column(banco.Integer)
    createdIn = banco.Column(banco.String(30))
    
    def __init__(self, id_comprador, id_vendor, id_item, preco): 
        self.id_comprador = id_comprador
        self.id_vendor = id_vendor
        self.id_item = id_item
        self.preco = preco
        self.createdIn = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def json(self):
        return{
            'id' : self.id,
            'id_comprador' : self.id_comprador,
            'id_vendor' : self.id_vendor,
            'id_item' : self.categoria,
            'preco' : self.preco                      
        }
    def save_transaction(self):
        banco.session.add(self)
        banco.session.commit()
        