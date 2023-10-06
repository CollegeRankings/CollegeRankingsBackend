from flask import Flask
from flask_restful import Api
import sys
sys.path.append("..")
from __init__ import app

api = Api(app=app)

@api.route("/helloworld/say")
def get_Helloworld():
    return "Helloworld"