from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'doggos bloggos ftw'

@app.route("/")
def hello():
    mysql = connectToMySQL('survey_with_valid')
    dojos = mysql.query_db('SELECT * FROM dojos;')

    return render_template("index.html", dojos = dojos)


@app.route('/process', methods=['POST'])
def process_user():
    is_valid = True
    if len(request.form['your_name']) < 1:
        is_valid = False
        flash("Please enter a valid name") 
    if len(request.form['your_location']) < 1:
        is_valid = False
        flash("Please enter a valid location")
    if len(request.form['favorite_language']) < 1:
        is_valid = False
        flash("Please select a favorite language")

    if not is_valid:
        return redirect('/')
    else:
        flash("User successfully added!")

        query = 'INSERT INTO dojos (name, location, language, created_at, updated_at) VALUES (%(your_name)s, %(your_location)s, %(favorite_language)s, NOW(), NOW());'
        data = {
            'your_name' : request.form['your_name'],
            'your_location' : request.form['your_location'],
            'favorite_language' : request.form['favorite_language']
        }
        dojos =connectToMySQL('survey_with_valid').query_db( query, data)
        return redirect('/show')


@app.route('/show')
def display():

    query = ('SELECT * FROM dojos;')

    dojos =connectToMySQL('survey_with_valid').query_db( query)

    return render_template("show.html", dojos = dojos)


if __name__=="__main__":
    app.run(debug=True)