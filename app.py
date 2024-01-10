from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPTokenAuth
import configuration
from users import Users
from db.db_tables import db_create
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


api.add_resource(LoginUser, "/login")
api.add_resource(CreateUser, "/user/register")
api.add_resource(ShowUser, "/user/get/<int:id>")
api.add_resource(DeleteUser, "/user/delete/<int:id>")

if __name__ == '__main__':
    db_create()
    app.run(debug=True, host='0.0.0.0')
