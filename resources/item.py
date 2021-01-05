from flask_restful import Resource, Api,reqparse
from flask_jwt import JWT,jwt_required
import sqlite3
from models.item import ItemModel



#resources will be external 
# api will work with apis and every resource has to be a class
# CRUD API

class  Item(Resource):
    # we need to authenticate before call get 
    #tell the server who you are
    # Postman: JWT ...
    #create parser object to parse data from request 
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type = float,
                        required=True,
                        help= 'price can not be None' 
                        #help: leave a message when something wrong
                        )
    #can also be used for html file 
    parser.add_argument('store_id',
                        type = int,
                        required=True,
                        help= 'Every item needs a store id.' 
                        #help: leave a message when something wrong
                        )
    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        #return {'item':None}, 404 # 404 is error code not found,
        return {'mesasge':'Item not found'},404
    #most popular status = 200 
    #created = 201
    #delaying creation = 202
    #unauthorize = 401 



    def post(self,name):
        #error first design
        # what if item is already exists 
        if ItemModel.find_by_name(name):
            return{'message':"An item wih name '{}' already exists".format(name)},400
        # bad request = 400
        
        data = Item.parser.parse_args() #version 2
        
        #you don't know what will user give you, and you can't give user an error
        # setting force = True: always processing the text 
        # setting silent = True: return None if the text is not as expected    
        
        item = ItemModel(name,data['price'],data['store_id'])

        #need to deal with exceptions here 
        try:
            item.save_to_db()
        #except runs  after self.insert(item) give an error message 
        except:
            return{'message':'an error occured inserting'},500 #500:internal server error 

        #example  if you post {'price':12},then data['price'] == {'chair':12}              
        #items.append(item)        
        return item.json() ,201
    


    #when run postman: you should set head:Authorization JWT:access_token  
    @jwt_required()
    def delete(self,name):
        item =ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'item deleted'}


    def put(self,name):
        data = Item.parser.parse_args()
        #item = next(filter(lambda x: x['name']==name,items),None)
        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(name,data['price'],data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()  


class Itemlist(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
        #return {'items':list(map(lambda x: x.json(),ItemModel.query.all()))}
