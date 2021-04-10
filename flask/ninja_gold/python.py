from flask import Flask, render_template, session, request, redirect
import random, datetime

app = Flask(__name__)
app.secret_key= 'password12345678'

@app.route('/')
def ninja_gold():
    if 'gold' not in session:
        session['gold'] = 0
    if 'activities' not in session:
        session['activities'] = []

    return render_template('index.html')

@app.route('/process_money', methods=['POST'])
def submit_form():
    if request.form['option']=='farm':
        session['tendies'] = random.randint(10,20)
        session['activities'].append([f"Earned {session['tendies']} gold from the farm! ({datetime.datetime.now().strftime('%c')})",'green'])
    elif request.form['option']=='cave':
        session['tendies'] = random.randint(5,10)
        session['activities'].append([f"Earned {session['tendies']} gold from the cave! ({datetime.datetime.now().strftime('%c')})",'green'])
    elif request.form['option']=='house':
        session['tendies'] = random.randint(1,5)
        session['activities'].append([f"Earned {session['tendies']} gold from the house! ({datetime.datetime.now().strftime('%c')})",'green'])
    elif request.form['option']=='casino':
        session['tendies'] = random.randint(-50,50)
        if session['tendies'] < 0:
            session['activities'].append([f"Entered a casino and lost {session['tendies']*-1} gold...Ouch! ({datetime.datetime.now().strftime('%c')})",'red'])
        else:
            session['activities'].append([f"Entered a casino and won {session['tendies']} gold...GG! ({datetime.datetime.now().strftime('%c')})",'green'])

    session['gold']+= session['tendies']
    return redirect('/')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)