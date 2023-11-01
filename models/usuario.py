from sql_alchemy import banco
from datetime import datetime

class UserModel(banco.Model):
    __tablename__ = 'users'
    user_id = banco.Column(banco.Integer, primary_key = True)
    login = banco.Column (banco.String(40))
    password = banco.Column (banco.String)
    email = banco.Column (banco.String)
    status = banco.Column (banco.Integer)
    type = banco.Column(banco.Integer)
    createdIn = banco.Column(banco.String(30))
    deleted_at = banco.Column(banco.String, default=None, nullable=True)
   
    
    def __init__(self, login, password, email, status, type):
        self.login = login
        self.password = password
        self.email = email
        self.status = status
        self.type = type
        self.createdIn = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        

    def json(self):
            return {
                'user_id': self.user_id,
                'login': self.login,
                'password':self.password,
                'status': self.status,
                'email': self.email,                
                'type': self.type,
                'createdIn': self.createdIn,
                }
     
    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id = user_id).first() #SELECT * FROM users WHERE user_id = user_id
        if user:
            return user
        return None
    
    
    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login = login).first()
        if user:
            return user
        return None
    
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()
        
    def update_user(self,user):
        self.login = user.login
        self.password = user.password
        self.type = user.type       
       
    
    def delete_user(self):
        self.status = 0 
        self.deleted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try: 
            banco.session.commit()
        except Exception as e:
            raise Exception(str(e))
        