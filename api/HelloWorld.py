from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, request, Resource # used for REST API building
import requests  # used for testing 
import random
from __init__ import login_manager, app, db
from model.collegeRankingsModels import College


helloworld_api = Blueprint('helloworld', __name__,
                   url_prefix='/api/helloworld')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(helloworld_api)

class HelloWorldAPI:
    # not implemented
    class _GetHello(Resource):
        def get(self, firstname):
            return "Hello World - " + firstname.upper() + request.args.get("lastname")
        
    class _RegisterAccount(Resource):
        def get(self):
            username = request.args.get("username")
            email = request.args.get("email")
            password = request.args.get("password")
            # Call a python function which takes these 3 values and creates a user record and saves into database
            return "Username: " + username
        
    class _addTwonumbers(Resource):
        def get(self):
            return "Sum: " + request.args.get("num1") + " + " + request.args.get("num2") + " = " + str(int(request.args.get("num1"))+int(request.args.get("num2")))

    """class _getCollege(Resource):
        def get(self):
            first_college = db.session.query(College).first()
            return first_college.name"""

    # building RESTapi resources/interfaces, these routes are added to Web Server
    api.add_resource(_GetHello, '/say/<string:firstname>')
    api.add_resource(_RegisterAccount, '/register')
    api.add_resource(_addTwonumbers, '/add')
    # api.add_resource(_getCollege, "/college")
