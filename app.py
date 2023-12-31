from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    age = db.Column(db.Integer)
    

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    name_len = db.Column(db.Integer)
    alexander = db.Column(db.Text)
    vladimir = db.Column(db.Text)
    dmitry = db.Column(db.Text)
    natalia = db.Column(db.Text)
    sofia = db.Column(db.Text)
    tatiana = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/questions')
def question_page():
    return render_template(
        'questions.html',
    )


with app.app_context():
    db.create_all()

@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    gender = request.args.get('gender')
    age = request.args.get('age')
    user = User(
        age=age,
        gender=gender
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    name_len = request.args.get('name_len')
    alexander = request.args.get('alexander')
    vladimir = request.args.get('vladimir')
    dmitry = request.args.get('dmitry')
    natalia = request.args.get('natalia')
    sofia = request.args.get('sofia')
    tatiana = request.args.get('tatiana')
    answer = Answers(id=user.id, name_len=name_len, alexander=alexander, vladimir=vladimir, dmitry=dmitry, 
                     natalia=natalia, sofia=sofia, tatiana=tatiana)
    db.session.add(answer)
    db.session.commit()
    return 'Анкета отправлена!'


@app.route('/stats')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['total_count'] = User.query.count()
    all_info['min_name_len'] = db.session.query(func.min(Answers.name_len)).one()[0]
    all_info['mean_name_len'] = db.session.query(func.avg(Answers.name_len)).one()[0]
    all_info['a_answers'] = ", ".join(re.findall(r'\w+', str(set(db.session.query(Answers.alexander).all()))))
    all_info['v_answers'] = ", ".join(re.findall(r'\w+', str(set(db.session.query(Answers.vladimir).all()))))
    all_info['d_answers'] = ", ".join(re.findall(r'\w+', str(set(db.session.query(Answers.dmitry).all()))))
    all_info['n_answers'] = ", ".join(re.findall(r'\w+', str(set(db.session.query(Answers.natalia).all()))))
    all_info['s_answers'] = ", ".join(re.findall(r'\w+', str(set(db.session.query(Answers.sofia).all()))))
    all_info['t_answers'] = ", ".join(re.findall(r'\w+', str(set(db.session.query(Answers.tatiana).all()))))
    return render_template('results.html', all_info=all_info)


if __name__ == '__main__':
    app.run()