from flask import Flask, render_template, session, request, redirect
import random 

app = Flask(__name__)
app.secret_key = 'shhhhhh_dontTell'

@app.route('/')
def main():
    session ['randint'] = random.randint(1,100)
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    if int(request.form['guess']) == session['randint']:
        response = "Nice! You done did it!"
        return render_template("index.html", response = response)
    elif int(request.form['guess']) > session['randint']:
        response = "That guess, is TOO damn high!"
        return render_template("index.html", response = response)
    elif int(request.form['guess'])< session['randint']:
        response = "Too low, once more, with FEELING!"
        return render_template("index.html", response = response)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)