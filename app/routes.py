
from app import app, db, lm 
from flask import Flask, render_template, request, session, redirect, flash, g
import models
import flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
import config
from flask.ext.login import LoginManager, url_for, login_user, logout_user, current_user, login_required

#is this where the query is made to the db which loads their data using a cookie set previously? 
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
    
@app.before_request
def before_request():
    #g.user = current_user
    g.user = models.User.query.get(1)
    
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
    try:
        studio = (flask.request.form['studio'])
        instructor = (flask.request.form['instructor'])
        before = (flask.request.form['before'])
        during = (flask.request.form['during'])
        after = (flask.request.form['after'])
        workout = Workout(studio=studio, instructor=instructor, before=before, during=during, after=after)
        g.user.workouts.append(workout)
        #db.session.add(workout)
        db.session.commit()
    except:
        return render_template("submit_workout.html", studio="", instructor="", before="", during="", after="", error="Your workout log wasn't complete! Please try again!")    
    return render_template("submit_workout.html", studio=studio, instructor=instructor, before=before, during=during, 
        after=after, error="")
      
@app.route('/profile')
#@login_required
def profile():
    workouts = g.user.workouts
    #workouts = models.Workout.query.all()
    return render_template('profile.html', workouts=workouts, user=g.user)
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))      

 
if __name__ == '__main__':
  app.run(debug=True)