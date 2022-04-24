from flask import Flask, render_template
from flask_login import LoginManager
from data import db_session
from data.users import User
from data.products import Products

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# login_manager = LoginManager()
# login_manager.init_app(app)


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