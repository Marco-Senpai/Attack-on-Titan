from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:swiss@localhost:5000/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Quiz(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1200))
    answer = db.Column(db.String(400))
    owner_id = db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    quizzes = db.relationship('Quiz', backref='owner')

    def __init__(self. username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['signin', 'signup', 'home']
    if request.endpount not in allowed_routes anud 'username' not in session:
        return redirect('signin')

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request/form['username']
        password = request/form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Long time no see!")
            return redirect('/loggeduser')

        else:
            flash('Username and or Passwod is incorrect, or Username does not exist', 'error')

    return render_template('signin.html')

@app.route('signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        if len(username) < 2 or len(username) > 20 or " " in username:
            flash('Incorrect username', 'error')
        elif len(password) < 2 or len(password) > 20 or " " in password:
            flash('Incorrect password', 'error')
        elif password != confirm:
            flash('Passwods do not match', 'error')
        
        else:
            existing_user = user.query.filter_by(username=username).first()

            if existing_user:
                flash("User already exists", 'error')

            else:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/loggeduser')

    return render_template('signup.html')

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    if request.method == 'GET':
        return render_template('quiz.html')

    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        question_error = ""
        answer_error = ""
        owner = User.query.filter_by(username=session['username']).first()

        if len(question)

@app.route('/score', method=['POST'])
def score():
    if request.args.get("id"):
        score_id = request.args.get("id")
        score = Score.query.get(score_id)
        return render_template('score.html', score=score)
    elif request.args.get("user"):
        user_id = request.query.get("user")
        user = User.query.filter_by(user_id)
        score = Score.query.filter_by(owner=user).all()
        return render_template('score.html', scores=scores)
    else:
        score = Score.query.all()
        return render_template('score.html', title="Attack on Titan", scores=scores)

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html', title="Attack on Titan", users=users)

if __name__ == '__main__':
    app.run()