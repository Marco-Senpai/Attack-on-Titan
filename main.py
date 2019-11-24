from flask import Flask, request, redirect, render_template, session, flash 
from flask_sqlalchemy import SQLAlchemy
import random, copy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://attack-on-titan:titan@localhost:3306/attack-on-titan'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y2k'

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1200))
    answer = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, question, answer, owner):
        self.question = question
        self.answer = answer
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    quizzes = db.relationship('Quiz', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


# original_questions = {
#     'What is the main protagonists name?':['Eren','Reiner','Sasha','Connie'],
#     'What do the titans do in the show?':['Eat people','Eat animals','Fight Gods','Work as slaves'],
#     'Where does the story take place?':['Behind a wall','In a warehouse','On the sea','In the mind of the protagonist'],

# }

# questions = copy.deepcopy(original_questions)

# def shuffle(q):
#     selected_keys = []
#     i = 0
#     while i < len(q):
#         current_selection = random.choice(q.keys())
#         if current_selection not in selected_keys:
#             selected_keys.append(current_selection)
#             i = i+1
#     return selected_keys

# @app.route('/quiz', methods=['POST', 'GET'])
# def quiz():
#     questions_shuffled = shuffle(questions)
#     for i in questions.keys():
#         random.shuffle(questions[i])
#     return render_template('main.html', q = questions_shuffled, o = questions)

@app.route('/score', methods=['POST'])
def score():
    correct = 0
    for i in questions.keys():
        answered = request.form[i]
        if original_questions[i][0] == answered:
            correct = correct+1
    return render_template('score.html')

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    if request.method == 'POST':
        

@app.before_request
def require_login():
    allowed_routes = ['signin', 'enlist', 'home','quiz']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/signin')

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Long time no see!")
            return redirect('/loggeduser')

        else:
            flash('Username and or Password is incorrect, or Username does not exist', 'error')

    return render_template('signin.html')

@app.route('/enlist', methods=['POST', 'GET'])
def enlist():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        if len(username) < 2 or len(username) > 20 or " " in username:
            flash('Incorrect username', 'error')
        elif len(password) < 2 or len(password) > 20 or " " in password:
            flash('Incorrect password', 'error')
        elif password != confirm:
            flash('Passwords do not match', 'error')
        else:
            existing_user = User.query.filter_by(username=username).first()

            if existing_user:
                flash("User already exists", 'error')

            else:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/loggeduser')

    return render_template('enlist.html')
        

@app.route('/signout', methods=['GET'])
def signout():
    if 'username' in session:
        del session['username']
        flash('sayonara')
        return redirect('/home')

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html', title="Attack on Titan", users=users)

if __name__ == '__main__':
    app.run()