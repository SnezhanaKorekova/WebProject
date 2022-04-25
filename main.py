from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required
from data import db_session
from data.users import User
from data.products import Products
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/')
@app.route('/index')
def index():
    db_session.global_init("db/products.db")
    db_sess = db_session.create_session()
    products = []
    for product in db_sess.query(Products).all():
        products.append((product.title, product.composition, product.price, product.path_to_photo))
    return render_template('index.html', products=products)


def add_user(surname, name, email, phone):
    user = User()
    user.surname = surname
    user.name = name
    user.email = email
    user.phone = phone
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def add_product(title, composition, price, path_to_photo):
    product = Products()
    product.title = title
    product.composition = composition
    product.price = price
    product.path_to_photo = path_to_photo
    db_sess = db_session.create_session()
    db_sess.add(product)
    db_sess.commit()


def main():
    # db_session.global_init("db/products.db")
    # db_sess = db_session.create_session()

    app.run()


if __name__ == '__main__':
    main()