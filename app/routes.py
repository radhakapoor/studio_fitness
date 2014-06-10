
from app import app, db, lm 
from flask import Flask, render_template, request, session, redirect, flash, g
#import models
import flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
import config
from flask.ext.login import LoginManager, url_for, login_user, logout_user, current_user, login_required
from sqlalchemy import Column, Integer, String

class Workout(db.Model):
    __tablename__='workout'
    id = db.Column(Integer, primary_key=True)
    studio = db.Column(String)
    instructor = db.Column(String)
    before = db.Column(Integer)
    during = db.Column(Integer)
    after = db.Column(Integer)
    owner_id = db.Column(Integer, db.ForeignKey('app_user.id'))
    
    def __init__(self, studio, instructor, before, during, after):
        self.studio = studio
        self.instructor = instructor
        self.before = before
        self.during = during
        self.after = after
        
    def __repr__(self):
        return '<I worked out at {} with {}. I felt {} before, {} during and {} after'.format(self.studio, self.instructor, self.before, self.during, self.after)
        
class User(db.Model):
    __tablename__='app_user'
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
        
#is this where the query is made to the db which loads their data using a cookie set previously? 
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
    
@app.before_request
def before_request():
    #g.user = current_user
    g.user = User.query.get(1)
    
@app.route('/login', methods=["GET"])
def get_login():
    if g.user:
        if not g.user.is_anonymous():
            return redirect("/logworkout")
    return render_template("login.html")
    
@app.route('/login', methods=["POST"])
def post_login():
    remember_me = request.form.get("remember_me")
    email = request.form.get("email")
    user = User.query.filter(User.email == email).first()
    if user:
        login_user(user, remember = remember_me)
        return redirect("/logworkout")
    else:
        return render_template("login.html", error="Invalid login")        
        
@app.route('/')   
def home():
  return render_template('home.html')
  
@app.route('/logworkout', methods=['GET'])
#@login_required
def get_logworkout():
    return render_template('log_workout.html', user=g.user)

@app.route('/logworkout', methods=['POST'])
#@login_required
def post_logworkout():
    studio_error = None
    instructor_error = None
    before_error = None
    during_error = None
    after_error = None
    general_error = None    
    studio = request.form.get('studio', None)
    if str(studio) == 'Select a Studio':
        studio = None
    instructor = request.form.get('instructor', None)
    if str(instructor) == 'Select an Instructor':
        instructor = None
    before = request.form.get('before', None)
    during = request.form.get('during', None)
    after = request.form.get('after', None)
       
    if studio is not None and instructor is not None and before is not None and during is not None and after is not None:
        workout = Workout(studio=studio, instructor=instructor, before=before, during=during, after=after)        
        g.user.workouts.append(workout)        
        db.session.commit()
        return render_template("submit_workout.html", studio=studio, instructor=instructor, before=before, during=during, 
        after=after, studio_error=studio_error, instructor_error=instructor_error, before_error=before_error, 
        during_error=during_error, after_error=after_error, general_error=general_error )
        
    elif studio is None and instructor is not None and before is not None and during is not None and after is not None:
        return render_template("log_workout.html", studio="", instructor="", before="", during="", 
        after="", studio_error="Error! Your workout log is incomplete! Please enter a studio.", instructor_error="", 
        before_error="", during_error="", after_error="", general_error="")
               
    elif studio is not None and instructor is None and before is not None and during is not None and after is not None:
        return render_template("log_workout.html", studio="", instructor="", before="", during="", 
        after="", studio_error="", instructor_error="Error! Your workout log is incomplete! Please enter an instructor.", 
        before_error="", during_error="", after_error="", general_error="")
        
    elif studio is not None and instructor is not None and before is None and during is not None and after is not None:
        return render_template("log_workout.html", studio="", instructor="", before="", during="", 
        after="", studio_error="", instructor_error="", before_error="Error! Your workout log is incomplete! Please enter how you felt *before* the workout.", 
        during_error="", after_error="", general_error="")
        
    elif studio is not None and instructor is not None and before is not None and during is None and after is not None:
        return render_template("log_workout.html", studio="", instructor="", before="", during="", 
        after="", studio_error="", instructor_error="", before_error="", during_error="Error! Your workout log is incomplete! Please enter how you felt *during* the workout.",
        after_error="", general_error="")
        
    elif studio is not None and instructor is not None and before is not None and during is not None and after is None:
        return render_template("log_workout.html", studio="", instructor="", before="", during="", 
        after="", studio_error="", instructor_error="", before_error="", during_error="", after_error="Error! Your workout log is incomplete! Please enter how you felt *after* the workout.", 
        general_error="")              
    else:
        return render_template("log_workout.html", studio="", instructor="", before="", during="", 
        after="", studio_error="", instructor_error="", before_error="", during_error="", after_error="", general_error="Error! Your workout log is incomplete!")    
                
  
@app.route('/profile')
#@login_required
def profile():
    workouts = g.user.workouts
    #workouts = models.Workout.query.all()
    return render_template('profile.html', workouts=workouts, user=g.user)
    
@app.route('/logout')
#@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))      

 
