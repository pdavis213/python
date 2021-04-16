from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)

#!  initial landing page
@app.route("/")
def index():
    mysql = connectToMySQL('ninjas_dojos')
    dojos = mysql.query_db('SELECT * FROM dojos')
    return render_template("index.html", dojos = dojos)


#!  adds new dojo to list
@app.route("/dojo", methods = ['POST'])
def add_dojo():
    mysql = connectToMySQL('ninjas_dojos')
    query = 'INSERT INTO dojos (name) VALUES (%(name)s);'
    data = {
        "name": request.form['name']
    }

    mysql.query_db(query,data)
    return redirect ("/")


#!  redirects to individual dojo info page
@app.route("/dojos_info/<int:dojos_id>")
def dojo_info(dojos_id):
    mysql = connectToMySQL("ninjas_dojos")
    query = 'SELECT * FROM ninjas JOIN dojos ON dojos.id  =  dojos_id WHERE dojos.id = %(dojos_id)s;'
    data = {
        'dojos_id' : dojos_id
    }

    dojos = mysql.query_db( query, data )
    
    return render_template("dojo_info.html", dojos = dojos)


#!  redirects to add ninja form
@app.route("/new_ninja")
def add_ninja():
    mysql = connectToMySQL('ninjas_dojos')
    dojos = mysql.query_db('SELECT * FROM dojos')
    return render_template("ninja_form.html", dojos = dojos)


#!  submits ninja to database
@app.route("/return_ninja", methods = ['POST'])
def submit_new_ninja():
    mysql = connectToMySQL("ninjas_dojos")
    query = 'INSERT INTO ninjas (first_name, last_name, age, created_at, updated_at, dojos_id) VALUES (%(first_name)s,%(last_name)s,%(age)s,NOW(),NOW(),%(dojos_id)s);'
    data = {
        "dojos_id" : request.form["dojos"],
        "first_name" : request.form["fname"],
        "last_name" : request.form["lname"],
        "age" : request.form["age"]
    }

    dojos = mysql.query_db( query, data )
    print(dojos)
    return redirect("/new_ninja")


if __name__ == "__main__":
    app.run(debug=True)