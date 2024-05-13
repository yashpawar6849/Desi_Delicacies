from flask import Flask, request, session, redirect, url_for

import random
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.asked_questions = {'easy': set(), 'medium': set(), 'hard': set()}  

    def start_quiz(self, theme):
        if theme.lower() in self.questions:
            session['theme'] = theme.lower()
            return redirect(url_for('quiz_route'))
        else:
            return "Invalid theme selected."

    def render_question(self):
        theme = session.get('theme')
        if theme is None:
            return "Please start the quiz first."

        available_questions = [q for q in self.questions[theme].items() if q[0] not in self.asked_questions[theme]]
        if not available_questions:
            return redirect(url_for('quiz_result'))
        else:
            question, _ = random.choice(available_questions)
            return '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Quiz</title>
            </head>
            <body>
                <h1>Quiz</h1>
                <p>{}</p>
                <form action="/quiz" method="post">
                    <label for="answer">Your Answer:</label>
                    <input type="text" id="answer" name="answer">
                    <button type="submit">Submit</button>
                </form>
            </body>
            </html>
            '''.format(question)

    def get_score(self):
        return self.score

    def get_congratulatory_message(self):
        if self.score >= 15:
            return "🎉 Congratulations! You're a QuizMaster Champion! 🎉"
        else:
            return "🚀 Keep practicing! You're on your way to becoming a QuizMaster! 🚀"

quiz = Quiz({
    'easy': {
        "What is 2 + 2?": "4",
        "Which planet is known as the Red Planet?": "mars",
        "What is the capital of Italy?": "rome",
        "What is the chemical symbol for gold?": "au",
        "How many continents are there in the world?": "7"
    },
    'medium': {
        "Who painted the Mona Lisa?": "leonardo da vinci",
        "What is the boiling point of water in Celsius?": "100",
        "What is the largest mammal in the world?": "blue whale",
        "What is the square root of 144?": "12",
        "Who is the author of 'To Kill a Mockingbird'?": "harper lee"
    },
    'hard': {
        "What is the speed of light in vacuum? (in meters per second)": "299792458",
        "What is the atomic number of oxygen?": "8",
        "What is the capital of Mongolia?": "ulaanbaatar",
        "What is the value of pi (π) correct to two decimal places?": "3.14",
        "Who discovered penicillin?": "alexander fleming"
    }
})

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to QuizMaster!</title>
    </head>
    <body>
        <h1>Welcome to QuizMaster!</h1>
        <p>Are you ready to test your knowledge? Click below to start the quiz:</p>
        <a href="/start">Start Quiz</a>
    </body>
    </html>
    '''

@app.route('/start', methods=['GET', 'POST'])
def start_quiz():
    if request.method == 'GET':
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Start Quiz</title>
        </head>
        <body>
            <h1>Start Quiz</h1>
            <form action="/start" method="post">
                <label for="theme">Select a theme:</label>
                <select id="theme" name="theme">
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                </select>
                <button type="submit">Start</button>
            </form>
        </body>
        </html>
        '''
    elif request.method == 'POST':
        theme = request.form['theme']
        return quiz.start_quiz(theme)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz_route():
    if request.method == 'GET':
        return quiz.render_question()
    elif request.method == 'POST':
        user_answer = request.form['answer']
        theme = session.get('theme')
        available_questions = [q for q in quiz.questions[theme].items() if q[0] not in quiz.asked_questions[theme]]
        if not available_questions:
            return redirect(url_for('quiz_result'))
        for question, correct_answer in available_questions:
            if user_answer.lower() == correct_answer.lower():
                quiz.score += 1
                quiz.asked_questions[theme].add(question)
                if len(quiz.asked_questions[theme]) == len(quiz.questions[theme]):
                    return redirect(url_for('quiz_result'))
                else:
                    return quiz.render_question()
        return "Invalid answer provided. Please try again."

@app.route('/result')
def quiz_result():
    score = quiz.get_score()
    message = quiz.get_congratulatory_message()
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Quiz Result</title>
    </head>
    <body>
        <h1>Quiz Result</h1>
        <p>Your score: {score}</p>
        <p>{message}</p>
        <a href="/">Back to Home</a>
    </body>
    </html>
    '''.format(score=score, message=message)

if __name__ == "__main__":
    app.run(debug=True)
