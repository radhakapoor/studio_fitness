from flask import Flask
from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import sqlite3


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'fitness.db'),
    DEBUG=True,
    SECRET_KEY='fitness',
    USERNAME='radhakapoor',
    PASSWORD='thinkful'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#hard code the username and password? 
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = "Invalid Password"
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('log_workout'))
    return render_template('login.html', error=error)


@app.route('/')   
def home():
  return render_template('home.html')


@app.route('/logworkout')
def log_workout():
    return render_template('log_workout.html')
    
@app.route('/profile')
def profile():
    return render_template('profile.html')
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))
    

 
if __name__ == '__main__':
  app.run(debug=True)