from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, request, Resource # used for REST API building
import requests  # used for testing
import random
from __init__ import login_manager, app, db
from model.collegeRankingsModels import College

college_api = Blueprint('college', __name__, url_prefix='/api/college')
# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1


api = Api(college_api)
class colleges:
    class _getColleges(Resource):
        def get(self):
            colleges = db.session.query(College).all()
            return jsonify([college.fewdetails() for college in colleges])
        
    class _getcollegedetails(Resource):
        def get(self):
            college = db.session.query(College).filter(College.id == int(request.args.get("id"))).first()
            return jsonify(college.alldetails())
        
    class _getrankingsCollege(Resource):
        def get(self):
            colleges = db.session.query(College).filter(College.ranking >= 3, College.ranking <= 5).limit(5)
            return jsonify([college.fewdetails() for college in colleges])

    
    api.add_resource(_getColleges, "/colleges")
    api.add_resource(_getcollegedetails, "/collegedetails")
    api.add_resource(_getrankingsCollege, "/mlrecommendation")
