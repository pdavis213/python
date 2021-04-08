from flask import Flask  #

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/dojo')
def dojo():
    return "Dojo"


@app.route('/say/<name>')
def greeting(name):
    print(name)
    return "Hi, " + name


@app.route('/repeat/<int:number>/<str>')
def repeat(number, str):

    return str * int(number)


if __name__ == "__main__":
    app.run(debug=True)
