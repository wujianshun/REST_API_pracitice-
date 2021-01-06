import os 
from flask import Flask,request
from flask_restful import Resource, Api,reqparse
#resources are Api can returned
#resources usually are mapped into database as well

#requparse is used for get the spicify data that you want
from flask_jwt import JWT,jwt_required

#JWT = json web token : to encoding some data 
from security import authenticate,identity

#item : package.lib 
from resources.item import Item,Itemlist
#register
from resources.user import UserRegister
from resources.store import Store,StoreList
from db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')

app.config['SQLALCHEMY_TRCK_MODIFICATIONS'] = False
#reason SQLalchemy_track has its own track which is better than track in Flask-sqlalchemy

#generate user key
app.secret_key = 'jose'


# make resources delete,post...easy
api = Api(app)
#user login 
#create new  endpoint
jwt = JWT(app,authenticate,identity) #/auth
#JWT is used for creating verification and giving authorization
# /auth  -> user:_   password:_
# receive acess_taken  


# route as argument(@method doesn't work)
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/sotres')
api.add_resource(Item,'/item/<string:name>') 
api.add_resource(Itemlist,'/items')
api.add_resource(UserRegister,'/register')


#goal: prevent run sth from import that we don't expected 
#python assign this file a name as '__main__'

#note:uwsgi will not run this part, so need to create new file to let app to run 

if __name__ =='__main__':
    db.init_app(app)
    app.run(port=5000,debug=True)

#test first design:better + efficient