from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL # import the function that will return an instance of a connection
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('users')# call the function, passing in the name of our db
    users = mysql.query_db('SELECT * FROM users;') # call the query_db function, pass in the query as a string
    print(users)
    return render_template("index.html", all_friends = users)

@app.route("/create_friend")
def add_friend_to_db():
    return render_template("create.html")
    

@app.route("/return_friend", methods = ["POST"])
def return_add():
    mysql = connectToMySQL("users")

    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }

    mysql.query_db(query, data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

