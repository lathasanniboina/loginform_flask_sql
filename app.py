from flask import Flask,request,render_template 
import pyodbc
import numpy as np
import pandas as pd
connection = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-D57LJRH;"
            "Database=latha;"
            "Trusted_Connection=yes;");# Creating Cursor    
    
cursor = connection.cursor()

app = Flask(__name__)
@app.route('/')
def login():
    return render_template('login.html')



@app.route('/validation_login',methods=['POST','GET'])
def validation_login():
    data=pd.read_sql_query('select * from p1',connection)
    mail=request.form['username']
    pwd=request.form['password']
    if mail not in list(data['email']):
	    return render_template('login.html',info='Invalid User')
    else:
        if pwd not in list(data['password']):
            return render_template('login.html',info='Invalid Password')
        else:
            name=list(data['name'])[list(data['email']).index(mail)]
            return render_template('home.html',name=name)
    

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/uplode_database",methods=['POST','GET'])
def uplode_database():
    name1=request.form['name']
    mail=request.form["email"]
    pwd=request.form['password']
    data=pd.read_sql_query('select * from p1',connection)
    if mail in list(data['email']):
	    return render_template('login.html',info='Alreaday User please login')
    cursor.execute("INSERT INTO p1 values ('{0}','{1}','{2}')".format(name1,mail,pwd))
    connection.commit()
    return render_template("home.html",name=name1)



if __name__ == '__main__':
    app.run(debug=True)