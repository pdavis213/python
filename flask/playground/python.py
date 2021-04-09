from flask import Flask, render_template
app = Flask(__name__)


@app.route("/play")
def index():
    return render_template("index.html")


@app.route("/play/<num>")
def renderBoxes(num):
    return render_template("renders.html", num=int(num))


@app.route("/play/<num>/<color>")
def colorize(num, color):
    return render_template("renders.html", num=int(num), color=color)


if __name__ == "__main__":
    app.run(debug=True)
