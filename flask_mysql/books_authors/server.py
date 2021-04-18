from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)



#! initial landing page - authors list
@app.route("/")
def index():
    mysql = connectToMySQL('authors_books')
    authors = mysql.query_db('SELECT * FROM authors')
    return render_template("index.html", authors = authors)



#!  adds new author to list
@app.route("/author", methods = ['POST'])
def submit_new_author():
    mysql = connectToMySQL('authors_books')
    query = 'INSERT INTO authors (name, updated_at, created_at) VALUES (%(name)s, NOW(), NOW());'
    data = {
        "name": request.form['name'],
    }

    mysql.query_db(query,data)
    return redirect ("/")



#! initial landing page - book list
@app.route("/book_list")
def display_books():
    mysql = connectToMySQL('authors_books')
    books = mysql.query_db('SELECT * FROM books')
    return render_template("books.html", books = books)



#!  adds new book to list
@app.route("/book", methods = ['POST'])
def submit_new_book():
    mysql = connectToMySQL('authors_books')
    query = 'INSERT INTO books (name, updated_at, created_at, num_of_pages) VALUES (%(name)s, NOW(), NOW(), %(num_of_pages)s);'
    data = {
        "name": request.form['name'],
        "num_of_pages": request.form['pages']
    }

    mysql.query_db(query,data)
    return redirect ("/book_list")



#!  Show Book
@app.route("/books_info/<int:book_id>")
def book_info(book_id):
    query = 'SELECT authors.name FROM authors JOIN book_favorites ON authors.id = book_favorites.author_id JOIN books ON books.id = book_favorites.book_id WHERE book_id = %(book_id)s;'
    query2 = 'SELECT * FROM authors'
    query3 = 'SELECT * FROM books WHERE id = %(book_id)s'
    data = {
        'book_id' : book_id
    }
    favorites = connectToMySQL("authors_books").query_db( query, data )
    name = connectToMySQL("authors_books").query_db( query2, data )
    title = connectToMySQL("authors_books").query_db( query3, data )

    return render_template("books_info.html", favorites = favorites, name = name, title = title)



#!  Add Favorites FROM BOOKS BOOK PAGE ONE NOT the other one
@app.route("/add_author/", methods = ['POST'])
def append_book():
    query = 'INSERT INTO book_favorites (author_id, book_id, created_at, updated_at) VALUES (%(author_id)s, %(book_id)s, NOW(), NOW());'
    data = {
            'author_id' : request.form['author_id'],
            'book_id' : request.form['book_id']
        }
    print(data)
    favorites = connectToMySQL('authors_books').query_db(query, data)
    return redirect(f"/books_info/{request.form['book_id']}")


#!  Show Author
@app.route("/authors_info/<int:author_id>")
def author_info(author_id):

    query = 'SELECT * FROM books JOIN book_favorites ON books.id = book_favorites.book_id JOIN authors ON authors.id = book_favorites.author_id WHERE author_id = %(author_id)s;'
    query2 = 'SELECT * FROM authors WHERE id = %(author_id)s'
    query3 = 'SELECT * FROM books'
    data = {
        'author_id' : author_id
    }

    favorites = connectToMySQL("authors_books").query_db( query, data )
    name = connectToMySQL("authors_books").query_db( query2, data )
    books = connectToMySQL("authors_books").query_db( query3, data )

    return render_template("author_favorites.html", favorites = favorites, name = name, books = books)



#! Add favorite to author
@app.route("/add_favorite/", methods =['POST'])
def append_author():
    query = 'INSERT INTO book_favorites (author_id, book_id, created_at, updated_at) VALUES ( %(author_id)s , %(book_id)s, NOW(), NOW() );'
    data =  {
        'author_id': request.form['author_id'],
        'book_id': request.form['favorites']
    }
    print(data)
    authors = connectToMySQL('authors_books').query_db(query, data)
    return redirect(f"/authors_info/{request.form['author_id']}")



if __name__ == "__main__":
    app.run(debug=True)

