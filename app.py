from flask import (Flask, g, render_template, redirect, flash, url_for)
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import config
import models
import forms


app = Flask(__name__)
app.secret_key = 'dwkfhr9ofnjfb2e'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close database connection after each connection"""
    g.db.close()
    return response


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('Your email or password doesnt match!', 'error')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You have been logged in!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Your email or password doesnt match!', 'error')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('You are registered!', 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            city=form.city.data,
            street=form.street.data,
            house_number=form.house_number.data,
            flat_number=form.flat_number.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/main', methods=('GET', 'POST'))
@login_required
def index():
    form = forms.FeesForm()
    statistic = None
    try:
        stat = models.UsersStatistics.select().where(
            models.UsersStatistics.user == current_user.id
        )
    except models.DoesNotExist:
        flash('Записей не найдено')
    else:
        statistic = stat
    if form.validate_on_submit():
        models.UsersStatistics.add_fee(
            user=g.user._get_current_object(),
            interval=form.interval.data,
            hot_water=form.hot_water.data,
            cold_water=form.cold_water.data,
            gas=form.gas.data,
            electricity=form.electricity.data
        )
        return redirect(url_for('index'))
    return render_template('main.html', form=form, stat=statistic)


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='yasik',
            email='yc@ya.ru',
            password='pass',
            city='Пермь',
            street='Механошина',
            house_number=4,
            flat_number=40,
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=config.DEBUG, port=config.PORT, host=config.HOST)
