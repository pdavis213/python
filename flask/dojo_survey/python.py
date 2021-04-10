from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")


@app.route('/users', methods=['post'])
def create_user():
    return render_template("show.html", name = request.form['your_name'],
    location = request.form['your_location'], language = request.form['favorite_language'], comment = request.form['comment'])


if __name__=="__main__":
    app.run(debug=True)