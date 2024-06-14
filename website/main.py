# main.py
from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import sys
import game
app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

score=0
price=0
change_question=1
@app.route('/')
def index():
    return render_template('index.html')
#image_folder_path = 'myenv/website/images/frontpage.jpg';
@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    global score
    global change_question
    global price
    username = request.form['username']
    user_answer = request.form.get('answer')
    action = request.form.get('action')

    if request.method == 'POST' and not user_answer:
        current_question=game.getQuestion()
        current_options=game.getOption()
        return render_template('quiz.html', username=username, question=current_question, options=current_options, useranswer=user_answer)

    elif request.method == 'POST' and user_answer:
        print("user_answer:",user_answer)
        if action == '50-50':
        # Call the 50-50 lifeline logic from game module
            current_question = game.getQuestion()
            removed_option_1, removed_option_2 = game.use_50_50_lifeline()
            current_options = (removed_option_1, removed_option_2)
            
             # Assign a value to current_question here
            return render_template('quiz.html', username=username, question=current_question, options=current_options, useranswer=user_answer, action='50-50')
        returnValue = game.check_answer(request.form.get('answer'),username)

        if returnValue == 0: # user answer is incorrect
            print("Incorrect Answer")
            return render_template('game_over.html', username=username,score=score,price=price)
        
        elif returnValue == 1: # user answer is correct
            print("Correct Answer")
            current_question=game.getQuestion()
            current_options=game.getOption()
            score += 1
            price += 1000
            return render_template('quiz.html', username=username, question=current_question, options=current_options, useranswer=user_answer)
        
        elif returnValue == 2 and change_question==1: # change question
            current_question = game.getQuestion()
            current_options = game.getOption()
            change_question = change_question-1
            return render_template('quiz.html', username=username, question=current_question, options=current_options,useranswer=user_answer, action='change_question')

        elif returnValue==3 :
             pass
        else: # default
            print("Check the logic for checking success and failure")
    return "invalid response"
if __name__ == '__main__':
    app.run(debug=True, port=5004)


