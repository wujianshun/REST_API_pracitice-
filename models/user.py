import sqlite3
from db import db
#1. create user object 
#2. have ability that interact with SQLite
#3. class User is helper here, will not interact with server
#4. models is our internal representation of an entity

class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    #must match with __init__


    def __init__(self,username,password):
        self.username = username
        self.password = password
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    #notice using class User
    @classmethod
    def find_by_user_name(cls,username):
        return cls.query.filter_by(username = username).first()
        #select *from where username = username limit 1


    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id = _id).first()
