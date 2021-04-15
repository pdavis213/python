from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)

#!  initial landing page
@app.route("/")
def index():
    mysql = connectToMySQL('users')
    users = mysql.query_db('SELECT * FROM users;')
    return render_template("index.html", all_friends = users)


#!  create friend page
@app.route("/create_friend")
def add_friend_to_db():
    mysql = connectToMySQL('users')
    users = mysql.query_db('SELECT * FROM users;')
    # print(users.id)
    return render_template("create.html", users = users[0])


#!  new friend info edit and submit
@app.route("/return_friend/<int:user_id>", methods = ["POST"])
def return_add(user_id):
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"
    data = {
        'id': user_id,
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }
    user = connectToMySQL("users").query_db(query,data)
    print(user)
    return redirect (f"/display_friend/{user_id}")


#!  update friend
# @app.route("/update_friend/<int:user_id>", methods = ['POST'])
# def update(user_id):
#     query = "UPDATE users SET first_name = %(first_name)s , last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
#     data = {
#         'id' : user_id,
#         "first_name": request.form["first_name"],
#         "last_name": request.form["last_name"],
#         "email": request.form["email"]
#     }    
#     user = connectToMySQL("users").query_db(query,data)
#     print(user)
#     return redirect (f"/display_friend/{user_id}")


#!  remove friend
@app.route("/delete_friend/<user_num>")
def delete(user_num):
    query = "DELETE FROM users WHERE id = %(user_num)s;"
    mysql = connectToMySQL("users")
    
    data = {
        'user_num' : user_num
        }
    users = mysql.query_db(query,data)
    print(users)
    return redirect("/")


#!  show individual friend
@app.route("/display_friend/<int:user_id>")
def friend_details(user_id):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        'id' : user_id
        }
    
    friend = connectToMySQL("users").query_db(query,data)
    # users = mysql.query_db(query,data)

    return render_template("friend.html", friend = friend)


#!  edit friends page
@app.route("/edit_friend/<int:user_id>")
def edit_friend(user_id):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        'id' : user_id
        }
    
    friend = connectToMySQL("users").query_db(query,data)
    return render_template("edit_friend.html", friend = friend[0])


#!  update friend
@app.route("/update_friend/<int:user_id>", methods = ['POST'])
def update(user_id):
    query = "UPDATE users SET first_name = %(first_name)s , last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
    data = {
        'id' : user_id,
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }    
    user = connectToMySQL("users").query_db(query,data)
    print(user)
    return redirect (f"/display_friend/{user_id}")


if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/remove_friend")
# def remove_friend(id):
#     mysql = connectToMySQL("users")

#     query = "REMOVE FROM users WHERE id = [0]"

#     return redirect("/")


