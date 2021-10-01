import os
import random
from flask import Flask, render_template, request, redirect, session, flash, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECEST_KEY', 'for dev')


@app.route('/')
def number():
    session['number'] = random.randint(1, 100)
    session['attemped'] = 1
    print(session['number'], " this is number")
    return render_template('index.html')


@app.route('/guess', methods=['POST'])
def guess_number():
    print('attemoed',  session['attemped'], " times")
    guessing_number = int(request.form['number'])
    if(guessing_number < 1 or guessing_number > 100):
        flash(" Your number should be between 1 - 100")
        return redirect(url_for('number'))
    else:
        if session['attemped'] > 5:
            return redirect('/game_over')
        if guessing_number < session['number']:
            session['attemped'] += 1
            return redirect('/tooLow')
        elif guessing_number > session['number']:
            session['attemped'] += 1
            return redirect('/tooHigh')
        else:
            return redirect('/winner')


@app.route('/tooLow')
def to_low():
    return render_template('too_low.html')


@app.route('/tooHigh')
def to_high():
    return render_template('too_high.html')


@app.route('/game_over')
def game_over():
    return render_template('game_over.html')


@app.route('/play_again', methods=['POST'])
def play_again():
    session.clear()
    return redirect('/')


@app.route('/winner')
def winner():
    return render_template('winner.html')


@app.route('/add_name', methods=['POST'])
def add_name():
    session['name'] = request.form['name']
    print(session['name'], " this is name that user submit")
    return redirect('/show_winner')


@app.route('/show_winner')
def show_winner():
    name = session['name']
    attemped = session['attemped']
    return render_template('show_winner.html', name=name, attemped=attemped)


if __name__ == "__main__":
    app.run(debug=True)
