from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL 
import re
app = Flask(__name__)
app.secret_key = 'doggos bloggos'
EMAIL_REGEX = re.compile('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



@app.route('/')
def home():
    mysql = connectToMySQL('emails')
    emails = mysql.query_db('SELECT * FROM emails;')

    return render_template("email_form.html", emails = emails)


@app.route('/process', methods=['POST'])
def submit():
    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!")

    if len(request.form['email'])< 1:
        is_valid = False
        flash("Email field cannot be left blank")

    if not is_valid:
        return redirect('/')

    else:
        flash("Database successfully updated.")

        query = 'INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s,NOW(), NOW());'
        data = {
            'email' : request.form['email']
        }

        user = connectToMySQL('emails').query_db(query, data)
        return redirect("/list")


@app.route('/list')
def show():

    query = ('SELECT * FROM emails;')
    emails = connectToMySQL('emails').query_db(query)

    return render_template("list.html", emails = emails)

if __name__=="__main__":
    app.run(debug=True)