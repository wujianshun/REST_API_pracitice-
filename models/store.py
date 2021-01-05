#classicmethod could be in models 
#resources should only interact with API
from db import db

class StoreModel(db.Model):
    __tablename__ ='stores'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80))
    
    items = db.relationship('ItemModel',lazy = 'dynamic')

    def __init__(self,name):
        self.name = name 


    def json(self):
        return{'name':self.name,'items':[item.json() for item in self.items.all()]}


    def save_to_db(self):
        #session:collections of object write into database
        # for update and insert 
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name = name).first()
        #select * from where name = name limit 1 
    

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()