from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPTokenAuth
import configuration
from users import Users
import secrets

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')
app.config['JSON_AS_ASCII'] = False
api = Api(app)

@auth.verify_token
def verify_token(token):
    user = Users()
    user.user_valid_token = token
    return bool(user.user_valid_token
                ) or token == configuration.ADMIN_TOKEN

class GetHealth(Resource):
    @auth.login_required
    def get(self):
        return "OK", 200

class LoginUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_uid")
        parser.add_argument("user_password")    
        params = parser.parse_args()
        user = Users()
        user.user_uid = params['user_uid']
        user.user_token = params['user_password']

        if user.user_token:
            response = jsonify({'user_token': user.user_token})
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return make_response(response, 201)
        return "Invalid UID or password", 403

class ShowUser(Resource):
    @auth.login_required
    def get(self, id=0):
        user = Users()
        user.user_uid = id
        user_map = user.user_map
        if user_map:
            response = jsonify(user_map)
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return make_response(response, 200)
        return "User not found", 404

class CreateUser(Resource):
    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("first_name")
        parser.add_argument("last_name")
        parser.add_argument("city")
        parser.add_argument("sex")
        parser.add_argument("age")
        parser.add_argument("hobbie")
        parser.add_argument("password")
        params = parser.parse_args()
        
        user = Users()
        user.user_map = {
            'first_name': params['first_name'],
            'last_name': params['last_name'],
            'city': params['city'],
            'sex': params['sex'],
            'age': params['age'],
            'hobbie': params['hobbie'],
            'password': params['password'],
            'token': secrets.token_hex(16)
        }
        
        
        response = jsonify({'user_uid': user.user_map['uid']})
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return make_response(response, 201)

class DeleteUser(Resource):
    @auth.login_required
    def delete(self, id):
        user = Users()
        user.user_uid = id

        del user.user_uid
        return user.user_map, 200

class FindUser(Resource):
    @auth.login_required
    def get(self):
        fname = request.args.get('first_name', '')
        lname = request.args.get('last_name', '')
        if len(fname) < 3 > len(lname):
            return "Length must be more than three characters", 400

        user = Users()
        print(fname, lname)
        user.user_first_name = fname
        user.user_last_name = lname
        found_users = user.user_find
        if found_users:
            response = jsonify(found_users)
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return make_response(response, 200)
        return "Users not found", 404

class UserPosts(Resource):
    @auth.login_required
    def get(self):
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 10))
        user = Users()
        user.user_friend_posts = (offset, limit)
        posts = user.user_friend_posts
        response = jsonify(posts)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return make_response(response, 200)

api.add_resource(GetHealth, "/health")
api.add_resource(LoginUser, "/login")
api.add_resource(CreateUser, "/user/register")
api.add_resource(ShowUser, "/user/get/<int:id>")
api.add_resource(DeleteUser, "/user/delete/<int:id>")
api.add_resource(FindUser, "/user/search")
api.add_resource(UserPosts, "/post/feed")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
