from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt        
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
bcrypt = Bcrypt(app) 
app.secret_key = 'doggos bloggos'


#!          initial landing page                 #!
@app.route('/')
def index():
    return render_template("landing_page.html")


#!          sumbision and checks for users registration         #!
@app.route('/register', methods=['POST'])
def create_user():
    if len(request.form['first']) < 1:
        flash('Please enter first name', 'First Name Error:')
    if not request.form['first'].isalpha():
        flash("First name may only contain letters", 'Naming Convention Error:')
    if len(request.form['last']) < 1:
        flash('Please enter last name', 'Last Name Error:')
    if not request.form['last'].isalpha():
        flash("Last name may only contain letters", 'Naming Convention Error:')
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Please enter a valid email address', 'Invalid Email Address!')
    if len(request.form['pass']) < 8:
        flash('Password must be at least 8 characters', 'Invalid Password!')
    if request.form['confirm_pass'] != request.form['pass']:
        flash('Passwords do not match!', 'Password Error:')
    if not '_flashes' in session.keys():
        flash('Friend successfully added!')
        pw_hash = bcrypt.generate_password_hash(request.form['pass'])
        # print(pw_hash)
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW())"
        data = {
            "first_name":request.form['first'],
            "last_name": request.form['last'],
            "email": request.form['email'],
            "password": pw_hash
        }
        mysql = connectToMySQL('users')
        result = mysql.query_db(query,data)
        # print(result)
        session['id'] = result
        return redirect('/success')
    else:
        return redirect('/')



#!          submission and checks for login attempt                  #!
@app.route('/login', methods=['POST'])
def login_user():
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {
        "email": request.form['email'],
    }
    mysql = connectToMySQL('users')
    result = mysql.query_db(query,data)


    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            flash("Logged in successfully added!")
            session['id'] = result[0]['id']
            return redirect('/success')
    return redirect("/")



#!          successful login page                 #!
@app.route('/success')
def success():
    if 'id' not in session:
        return redirect("/")
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        "id": session['id'],
    }
    mysql = connectToMySQL('users')
    result = mysql.query_db(query,data)

    session['name'] = f"{result[0]['first_name']} {result[0]['last_name']}"
    return render_template("successful_login.html")


#!          logout action                 #!
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

if __name__=='__main__':
    app.run(debug=True)



# Checks as a function if needed for future assignments
# def validate_recipe(recipe):
#     is_valid = True
#     if len(recipe['name']) <3:
#         is_valid = False
#         flash("Recipe name must be at least 3 characters", "recipe")
#     if len(recipe['description']) <3:
#         is_valid = False
#         flash("Recipe description must be at least 3 characters", "recipe")
#     if len(recipe['instructions']) <3:
#         is_valid = False
#         flash("Recipe instructions must be at least 3 characters", "recipe")
#     if recipe['under_thrity'] == None:
#         is_valid = False
#         flash("Please select if recipe is under 30 minutes", "recipe")
#     return is_valid
