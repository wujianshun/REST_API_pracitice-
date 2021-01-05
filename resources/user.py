import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel 
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type = str,
    required=True,
    help = 'This field can not be blank'
    )
    parser.add_argument('password',
    type = str,
    required=True,
    help = 'This field can not be blank'
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        #how to prevent registing with same username
        if UserModel.find_by_user_name(data['username']):
            return {'message':'A user with that username already exists'},400 
        #user = Usermodel(**data)       
        user = UserModel(data['username'],data['password'])
        user.save_to_db()
        return {'message':'user created successfully'}, 201 
