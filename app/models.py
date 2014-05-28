from routes import app, db
from sqlalchemy import Column, Integer, String


class Workout(db.Model):
    __tablename__='workout'
    id = db.Column(Integer, primary_key=True)
    studio = db.Column(String)
    instructor = db.Column(String)
    before = db.Column(Integer)
    during = db.Column(Integer)
    after = db.Column(Integer)
    owner_id = db.Column(Integer, db.ForeignKey('user.id'))
    
    def __init__(self, studio, instructor, before, during, after):
        self.studio = studio
        self.instructor = instructor
        self.before = before
        self.during = during
        self.after = after
        
    def __repr__(self):
        return '<I worked out at {} with {}. I felt {} before, {} during and {} after'.format(self.studio, self.instructor, self.before, self.during, self.after)
        
class User(db.Model):
    __tablename__='user'
    id = db.Column(Integer, primary_key=True)
    email = db.Column(String(200))
    workouts = db.relationship("Workout", backref="owner", lazy="dynamic")
    
    def __init__(self, email=None):
        self.email = email
        
    def __repr__(self):
        return "<User {}>".format(self.email)
        
    def get_id(self):
        return unicode(self.id)
        
    #not sure if need this   
    def is_authenticated(self):
        return True
        
    #not sure if need this
    def is_active(self):
        return True
        
    #not sure if need this    
    def is_anonymous(self):
        return False
        
    