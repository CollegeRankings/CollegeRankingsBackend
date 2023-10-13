from __init__ import login_manager, app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
import pandas as pd


@login_manager.user_loader
def load_user(account_id):
    return Account.query.get(account_id)


class Account(db.Model, UserMixin):
    __tablename__ = 'accounts'

    account_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # favoriteList = db.relationship("Product", backref='Person', uselist=True)
    password_hash = db.Column(db.String(128))
    favorites = db.relationship('Favorite', backref='Account', uselist=True, lazy='dynamic')

    def __init__(self, firstname, lastname, email, username, password):
        self.first_name = firstname
        self.last_name = lastname
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class College(db.Model, UserMixin):
    __tablename__ = 'colleges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=True)
    state = db.Column(db.String(8), index=True, nullable=True)
    city = db.Column(db.String(64), index=True, nullable=True)
    zip = db.Column(db.Integer, index=True, nullable=True)
    type = db.Column(db.String(64), index=True, nullable=True)
    image = db.Column(db.String(256), index=True, nullable=True)
    ranking = db.Column(db.Integer, index=True, nullable=True)
    ACTAvg = db.Column(db.Integer, index=True, nullable=True)
    aidpercent = db.Column(db.Integer, index=True, nullable=True)
    acceptance = db.Column(db.Integer, index=True, nullable=True)
    fees = db.Column(db.Integer, index=True, nullable=True)
    GPAAvg = db.Column(db.Float, index=True, nullable=True)
    enrollment = db.Column(db.Integer, index=True, nullable=True)
    SATAvg = db.Column(db.Integer, index=True, nullable=True)
    SATRange = db.Column(db.String(64), index=True, nullable=True)
    ACTRange = db.Column(db.String(64), index=True, nullable=True)
    YearFounded = db.Column(db.Integer, index=True, nullable=True)
    AcademicCalendar = db.Column(db.String(128), index=True, nullable=True)
    setting = db.Column(db.String(64), index=True, nullable=True)
    SchoolWebsite = db.Column(db.String(128), index=True, nullable=True)
    favorites = db.relationship('Favorite', backref='College', uselist=True, lazy='dynamic')

    def __init__(self, name, state, city, zip, type, image, ranking, ACTAvg, 
                 aidpercent, acceptance, fees, GPAAvg, enrollment, SATAvg, 
                 SATRange, ACTRange, YearFounded, AcademicCalendar, setting,
                 SchoolWebsite):
        self.name = name
        self.state = state
        self.city = city
        self.zip = zip
        self.type = type
        self.image = image
        self.ranking = ranking
        self.ACTAvg = ACTAvg
        self.aidpercent = aidpercent
        self.acceptance = acceptance
        self.fees = fees
        self.GPAAvg = GPAAvg
        self.enrollment = enrollment
        self.SATAvg = SATAvg
        self.SATRange = SATRange
        self.ACTRange = ACTRange
        self.YearFounded = YearFounded
        self.AcademicCalendar = AcademicCalendar
        self.setting = setting
        self.SchoolWebsite = SchoolWebsite
    
    def alldetails(self):
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "city": self.city,
            "zip": self.zip,
            "type": self.type,
            "image": self.image,
            "ranking": self.ranking,
            "ACTAvg": self.ACTAvg,
            "aidpercent": self.aidpercent,
            "acceptance": self.acceptance,
            "fees": self.fees,
            "GPAAvg": self.GPAAvg,
            "enrollment": self.enrollment,
            "SATAvg": self.SATAvg,
            "SATRange": self.SATRange,
            "ACTRange": self.ACTRange,
            "YearFounded": self.YearFounded,
            "AcademicCalendar": self.AcademicCalendar,
            "setting": self.setting,
            "SchoolWebsite": self.SchoolWebsite,
        }
    
    def fewdetails(self):
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "city": self.city,
            "image": self.image,
            "ranking": self.ranking
        }

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'))
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'))

    def __init__(self, account_id, college_id):
        self.account_id = account_id
        self.college_id = college_id


def initColleges():
    with app.app_context():
        """Create database and tables"""
        print("Creating college tables")
        db.create_all()
        college_count = db.session.query(College).count()
        if college_count > 0:
            return
        
        basedir = os.path.abspath(os.path.dirname(__file__))

        # Specify the file path
        file_path = basedir + "/../static/data/CollegeData.csv"
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Iterate through each row in the DataFrame and add to the colleges table
        for index, row in df.iterrows():
            try:
                college = College(
                    name=row['Name'] if pd.notna(row['Name']) else None,
                    state=row['State'] if pd.notna(row['State']) else None,
                    city=row['City'] if pd.notna(row['City']) else None,
                    zip=row['Zip'] if pd.notna(row['Zip']) else None,
                    type=row['Type'] if pd.notna(row['Type']) else None,
                    image=row['Image'] if pd.notna(row['Image']) else None,
                    ranking=row['Ranking'] if pd.notna(row['Ranking']) else None,
                    ACTAvg=row['ACT'] if pd.notna(row['ACT']) else None,
                    aidpercent=row['AidPercentage'] if pd.notna(row['AidPercentage']) else None,
                    acceptance=row['AcceptanceRate'] if pd.notna(row['AcceptanceRate']) else None,
                    fees=row['Fees'] if pd.notna(row['Fees']) else None,
                    GPAAvg=row['GPAAvg'] if pd.notna(row['GPAAvg']) else None,
                    enrollment=row['Enrollment'] if pd.notna(row['Enrollment']) else None,
                    SATAvg=row['SATAvg'] if pd.notna(row['SATAvg']) else None,
                    SATRange=row['SATRange'] if pd.notna(row['SATRange']) else None,
                    ACTRange=row['ACTRange'] if pd.notna(row['ACTRange']) else None,
                    YearFounded=row['YearFounded'] if pd.notna(row['YearFounded']) else None,
                    AcademicCalendar=row['AcademicCalendar'] if pd.notna(row['AcademicCalendar']) else None,
                    setting=row['Setting'] if pd.notna(row['Setting']) else None,
                    SchoolWebsite=row['SchoolWebsite'] if pd.notna(row['SchoolWebsite']) else None
                )
                db.session.add(college)
                db.session.commit()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate college, or error: {college.name}")
            except Exception as e_inner:
                print(f"Error adding college at index {index}: {str(e_inner)}")

