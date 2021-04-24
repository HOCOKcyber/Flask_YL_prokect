from flask import Flask, render_template, redirect
from flask_data.donate import DonateForm
from flask_data.login import LoginForm
from data import db_session, bot_api
from data.users import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
with open('Ключи.txt', 'rt') as f:
    KEY = str(f.readline().split()[1])
app.config['SECRET_KEY'] = KEY
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return render_template('home.html')
    return render_template('base.html')


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    form = DonateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.name == form.user_name.data).first():
            return render_template('donate.html', title='Донат', form=form, message="Пользователя не существует")
        user = db_sess.query(User).filter(User.name == form.user_name.data).first()
        user.score += int(form.donate.data) * 50
        db_sess.commit()
        return render_template('after_donate.html')
    return render_template('donate.html', title='Донат', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = LoginForm()
    if login.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.name == login.login.data).first():
            return render_template('login.html', title='Вход', login=login, message="Пользователя не существует", )
        user = db_sess.query(User).filter(User.name == login.login.data).first()
        login_user(user)
        return redirect("/")
    return render_template('login.html', title='Вход', login=login)


if __name__ == '__main__':
    db_session.global_init("db/bot.db")
    app.register_blueprint(bot_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
