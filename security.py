from werkzeug.security import safe_str_cmp
#safe way for comparing string 

from models.user import UserModel
#login user 
def authenticate(username,password):
    user = UserModel.find_by_user_name(username)
    if user and safe_str_cmp(user.password,password):
        return user 

#identity user
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)



