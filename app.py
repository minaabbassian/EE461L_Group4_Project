from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import userinfo_database as ud
import projectinfo_database as pd

app = Flask(__name__)

#main page
@app.route('/')
def hello_world():
    return render_template("login.html")
database={'nachi':'123','james':'aac','karthik':'asdsf'}

# login method prompting usernam and password
@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']

    valid = ud.isUserInfoCorrect(name1, pwd)
    if(valid = 'Found'):
        return render_template('home.html', name = name1)

    elif(valid = 'Password'):
        return render_template('login.html', info = 'Invalid Password')
    else: 
        return render_template('login.html', info = 'Invalid Username')
    
    # if name1 not in database:
	#     return render_template('login.html',info='Invalid User')
    # else:
    #     if database[name1]!=pwd:
    #         return render_template('login.html',info='Invalid Password')
    #     else:
	#          return render_template('home.html',name=name1)

#registering a new user
@app.route('/form_signup',methods=['POST','GET'])
def signup():
    name1=request.form['username']
    pwd=request.form['password']

    if (ud.isUsernameTaken(name1)):
        return render_template('login.html', info='Username Taken')
    else:
        ud.addNewUser(name1, pwd)

#creating a new project
@app.route('/form_createproject', methods=['POST', 'GET'])
def create():
    projId = request.form['projectId']
    desc = request.form['description']

    check = pd.addNewProjectToCollection(projId, desc, projId)
    if(check = "taken"):
        return render_template('home.html', info="ProjectId taken")


#signing into existing project
@app.route('/form_signintoproject', methods=['POST', 'GET'])
def signIn():
    projId = request.form['projectId']

    validate = pd.getExistingProject(projId)
    if(validate = "no"):
        return render_template('home.html', info='ProjectId not found')
    else:
        return render_template('home.html', info=validate)



if __name__ == '__main__':
    app.run()