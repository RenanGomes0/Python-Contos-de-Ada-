from sql_alchemy import banco
from datetime import datetime


class TransactionsModel(banco.Model):
    __tablename__ = 'transactions'
    
    id = banco.Column(banco.Integer, primary_key=True)
    comprador_id = banco.Column(banco.String(80))
    vendedor_id = banco.Column(banco.String(80))
    item_id = banco.Column(banco.String(80))
    preco = banco.Column(banco.Float(precision=2))
    createdIn = banco.Column(banco.String(30))
    
    def __init__(self, comprador_id, vendedor_id, item_id, preco): 
        self.comprador_id = comprador_id
        self.vendedor_id = vendedor_id
        self.item_id = item_id
        self.preco = preco
        self.createdIn = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def json(self):
        return {
            'id': self.id,
            'comprador_id': self.comprador_id,
            'vendedor_id': self.vendedor_id,
            'item_id': self.item_id,  # Corrigido de categoria para id_item
            'preco': self.preco                      
        }
    
    @classmethod
    def pesquisa_transactions(cls):
        transactions = cls.query.filter_by().all()
        if transactions:
            return transactions
        return None
    
    
    @classmethod
    def Pesquisa_transactions_comprador_id(cls, comprador_id):
        transactions = cls.query.filter_by(comprador_id = comprador_id).all()
        if transactions:
            return transactions
        return None


    def save_transaction(self):
        banco.session.add(self)
        banco.session.commit()

        