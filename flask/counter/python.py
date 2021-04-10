from flask import Flask, render_template, session, redirect

app = Flask(__name__)
app.secret_key = "encrypt"


@app.route('/')
def counter():
    if "count" not in session:
        session['count'] = 1
    else:
        session['count'] +=1
    return render_template("index.html")


@app.route('/destroy')
def reset():
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)