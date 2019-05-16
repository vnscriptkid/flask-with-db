from werkzeug.security import safe_str_cmp
from models.user import User
from werkzeug.security import check_password_hash

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and check_password_hash(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_userid(user_id)