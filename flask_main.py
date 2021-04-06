from flask import Flask, render_template, redirect
from login import DonateForm
from data import db_session
from data.users import User


app = Flask(__name__)
with open('Ключи.txt', 'rt') as f:
    KEY = str(f.readline().split()[1])
app.config['SECRET_KEY'] = KEY


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    form = DonateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.name == form.user_name.data).first():
            return render_template('donate.html', title='Донат',
                                   form=form,
                                   message="Пользователя не существует")

        user = db_sess.query(User).filter(User.name == form.user_name.data).first()
        user.score += int(form.donate.data) * 50
        db_sess.commit()
        return render_template('after_donate.html')
    return render_template('donate.html', title='Донат', form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')