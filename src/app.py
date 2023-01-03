import os
from flask import abort, flash, Flask, redirect, render_template, request, url_for
from flask_login import current_user, LoginManager, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm
from models import User, List


app = Flask(__name__)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
                flash('User added successfully', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                print(e)
                abort(500)
        else:
            flash('Invalid username or password', 'error')

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are successfully logged in', 'success')
        return redirect(url_for('index'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password', 'error')
                return render_template('login.html', form=form)
            login_user(user, remember=form.remember_me.data)
            flash('You are successfully logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been successfully logged out', 'success')
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', list=get_mylist())


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        rank = request.form.getlist('rank')
        content = request.form.getlist('content')
        comment = request.form.getlist('comment')

        if not current_user.is_authenticated:
            flash('Please login', 'error')
            return render_template('index.html', list=zip(rank, content, comment))

        if not validate_list(rank, content, comment):
            return render_template('index.html', list=zip(rank, content, comment))

        update_mylist(rank, content, comment)

    return redirect(url_for('index'))


def get_mylist():
    # initial values
    rank = [1, 2, 3]
    content = ['', '', '']
    comment = ['', '', '']

    rows = List.query.filter_by(user_id=current_user.get_id()).order_by(List.rank).all()

    if not rows:
        return zip(rank, content, comment)

    rank.clear()
    content.clear()
    comment.clear()

    for row in rows:
        rank.append(row.rank)
        content.append(row.content)
        comment.append(row.comment)

    return zip(rank, content, comment)


def update_mylist(rank, content, comment):
    try:
        db.session.query(List).filter_by(user_id=current_user.get_id()).delete()

        for row in range(len(rank)):
            if not rank[row] and not content[row] and not comment[row]:
                continue

            list = List(rank=rank[row], content=content[row], comment=comment[row], user_id=current_user.get_id())
            db.session.add(list)

        db.session.commit()

    except Exception as e:
        print(e)
        abort(500)


def validate_list(rank, content, comment):
    for row in range(len(rank)):
        if not rank[row].isnumeric() and rank[row] == '':
            flash('Rank must be a number', 'error')
            return False

        if int(rank[row]) < 0:
            flash('Rank must be greater than or equal to 0')
            return False

        if len(rank[row]) > 5:
            flash('Rank must be less than 6 characters', 'error')
            return False

        if len(content[row]) > 80:
            flash('Content must be less than 81 characters', 'error')
            return False

        if len(comment[row]) > 255:
            flash('Comment must be less than 256 characters', 'error')
            return False

    return True


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
