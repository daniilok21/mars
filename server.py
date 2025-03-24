from datetime import datetime
from flask import Flask, render_template, redirect
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.news import News
from forms.user import RegisterForm
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_session.global_init("blogs.db")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('jobs.html', jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Проверка паролей
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")

        # Инициализация базы данных
        db_session.global_init("mars_explorer.db")
        db_sess = db_session.create_session()

        # Проверка, существует ли пользователь с таким email
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь с таким email уже существует")

        # Создание нового пользователя
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
            hashed_password=generate_password_hash(form.password.data),
            about=form.about.data
        )
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')

    return render_template('register.html', title='Регистрация', form=form)


def example():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    # cap = User(
    #     surname="Scott",
    #     name="Ridley",
    #     age=21,
    #     position="captain",
    #     speciality="research engineer",
    #     address="module_1",
    #     email="scott_chief@mars.org",
    #     hashed_password="cap"
    # )
    # db_sess.add(cap)
    # user1 = User(
    #     surname="Markov",
    #     name="Mark",
    #     age=52,
    #     position="engineer",
    #     speciality="mechanical engineer",
    #     address="module_2",
    #     email="markov_mark@mars.org",
    #     hashed_password="eng"
    # )
    # db_sess.add(user1)
    # user2 = User(
    #     surname="Ivanov",
    #     name="Lexa",
    #     age=69,
    #     position="medic",
    #     speciality="surgeon",
    #     address="module_3",
    #     email="ivanov_lexa@mars.org",
    #     hashed_password="med"
    # )
    # db_sess.add(user2)
    # user3 = User(
    #     surname="Kjhbvc",
    #     name="Chjkl",
    #     age=30,
    #     position="hare",
    #     speciality="freeloader",
    #     address="module_4",
    #     email="kjhbvc_chjkl@mars.org",
    #     hashed_password="ha"
    # )
    # db_sess.add(user3)
    job = Jobs(
        team_leader=1,
        job="deployment of residential modules 1 and 2",
        work_size=15,
        collaborators="2, 3",
        start_date=datetime.now(),
        is_finished=False
    )
    db_sess.add(job)
    db_sess.commit()


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
