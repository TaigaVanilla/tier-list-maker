import os
from flask import abort, flash, Flask, redirect, render_template, request, url_for
from flask_login import current_user, LoginManager, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from forms import ListForm, LoginForm, RegistrationForm
from models import User, List


app = Flask(__name__)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

app.jinja_env.filters['zip'] = zip

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
                app.logger.error('An unexpected error has occurred: \n%s', e)
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
    try:
        return db.session.query(User).filter(User.id == id).one_or_none()
    except Exception as e:
        app.logger.error('An unexpected error has occurred: \n%s', e)
        abort(500)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ListForm()

    rank, content, comment = search_mylist()

    for i in range(len(rank)):
        form.rank.append_entry(rank[i])
        form.content.append_entry(content[i])
        form.comment.append_entry(comment[i])

    return render_template('index.html', form=form, zip=zip)


@app.route('/update', methods=['GET', 'POST'])
def update():
    form = ListForm()

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please login', 'error')
            return render_template('index.html', form=form, zip=zip)

        rank = form.rank.data
        content = form.content.data
        comment = form.comment.data

        if form.validate_on_submit():
            update_mylist(rank, content, comment)
        else:
            error_messages = []
            for field_name, field_errors in form.errors.items():
                for error_message in field_errors:
                    if error_message:
                        error_messages.append(error_message[0])
            # remove duplicates from error_messages list
            error_messages = list(dict.fromkeys(error_messages))
            return render_template('index.html', form=form, zip=zip, error_messages=error_messages)

    return redirect(url_for('index'))


def search_mylist():
    # initial values
    rank = [1, 2, 3]
    content = ['', '', '']
    comment = ['', '', '']

    try:
        rows = (
            db.session.execute(db.select(List).where(List.user_id == current_user.get_id()).order_by(List.rank))
            .scalars()
            .all()
        )

        if not rows:
            return rank, content, comment

        rank.clear()
        content.clear()
        comment.clear()

        for row in rows:
            rank.append(row.rank)
            content.append(row.content)
            comment.append(row.comment)

        return rank, content, comment

    except Exception as e:
        app.logger.error('An unexpected error has occurred: \n%s', e)
        abort(500)


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
        app.logger.error('An unexpected error has occurred: \n%s', e)
        abort(500)


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
