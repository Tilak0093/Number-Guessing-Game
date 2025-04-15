from flask import Flask, render_template, request, session, redirect, url_for, flash
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a real secret key in production

@app.route('/', methods=['GET', 'POST'])
def number_guessing_game():
    # Initialize game if not already started
    if 'secret_number' not in session:
        session['secret_number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['max_attempts'] = 10
        session['game_over'] = False
        session['guess_history'] = []
    
    if request.method == 'POST' and not session['game_over']:
        try:
            guess = int(request.form['guess'])
            if guess < 1 or guess > 100:
                flash("Please enter a number between 1 and 100!", 'error')
            else:
                session['attempts'] += 1
                session['guess_history'].append(guess)
                
                if guess < session['secret_number']:
                    flash("Too low! Try a higher number.", 'info')
                elif guess > session['secret_number']:
                    flash("Too high! Try a lower number.", 'info')
                else:
                    flash(f"🎉 Congratulations! You guessed the number {session['secret_number']} in {session['attempts']} attempts!", 'success')
                    session['game_over'] = True
                
                if session['attempts'] >= session['max_attempts'] and not session['game_over']:
                    flash(f"😢 Game over! The number was {session['secret_number']}. Better luck next time!", 'error')
                    session['game_over'] = True
                
        except ValueError:
            flash("Please enter a valid number!", 'error')
    
    return render_template('index.html', 
                         attempts=session['attempts'],
                         max_attempts=session['max_attempts'],
                         game_over=session['game_over'],
                         guess_history=session.get('guess_history', []))

@app.route('/reset')
def reset_game():
    session.clear()
    return redirect(url_for('number_guessing_game'))

if __name__ == '__main__':
    app.run(debug=True)