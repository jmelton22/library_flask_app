from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from forms import LoginForm, RegisterForm, EditProfile
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create database and import table classes
db = SQLAlchemy(app)
from models import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    form.library.choices = [(lib.library_id, lib.library_name) for lib in Library.query.order_by('library_name')]
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # noinspection PyArgumentList
        new_user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        password=hashed_password,
                        library_id=form.library.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))

    return render_template('register.html', title='Sign Up', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('index'))

        return '<h1>Invalid email or password</h1>'

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<user_id>')
@login_required
def user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    books = db.session.query(Book, Author, UserBook).join(Author).join(UserBook).filter_by(user_id=user_id).all()
    return render_template('user.html', user=user, books=books, today=datetime.now())


@app.route('/user/<user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    form = EditProfile(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()

        return redirect(url_for('user', user_id=user_id))

    return render_template('edit_user.html', user=user, form=form)


@app.route('/user/<user_id>/return/<book_id>')
def return_book(user_id, book_id, checkout_date):
    conn = db.session.connection()
    conn.execute(text("CALL return_book(:u_id, :b_id, :c_date)"),
                 u_id=user_id, b_id=book_id, c_date=checkout_date)
    db.session.commit()
    conn.close()
    return redirect(url_for('user', user_id=user_id))


@app.route('/books')
def books():
    result = db.session.query(Book, Author).join(Author).join(LibraryCatalog).order_by(Book.title).filter(LibraryCatalog.num_copies > 0).all()
    return render_template('books.html', books=result)


@app.route('/book/<book_id>')
def book(book_id):
    book, author, genre = db.session.query(Book, Author, Genre).join(Author).join(Genre).filter(Book.book_id == book_id).one()
    return render_template('book.html', book=book, author=author, genre=genre)


@app.route('/author/<author_id>')
def author(author_id):
    author = db.session.query(Author).filter(Author.author_id == author_id).one()
    books = db.session.query(Book).filter(Book.author_id == author_id).all()
    return render_template('author.html', author=author, books=books)


@app.route('/book/<book_id>/checkout', methods=['GET', 'POST'])
@login_required
def checkout(book_id):
    conn = db.session.connection()
    conn.execute(text("CALL checkout_book(:u_id, :b_id)"),
                 u_id=current_user.user_id, b_id=book_id)
    db.session.commit()
    conn.close()

    return redirect(url_for('book', book_id=book_id))


@app.route('/book/<book_id>/hold', methods=['GET', 'POST'])
@login_required
def hold(book_id):
    conn = db.session.connection()
    conn.execute(text("CALL hold_book(:u_id, :b_id)"),
                 u_id=current_user.user_id, b_id=book_id)
    db.session.commit()
    conn.close()

    return redirect(url_for('book', book_id=book_id))


@app.route('/user/<user_id>/renew/<book_id>')
def renew_book(user_id, book_id):
    conn = db.session.connection()
    conn.execute(text("CALL renew_book(:u_id, :b_id)"),
                 u_id=user_id, b_id=book_id)
    db.session.commit()
    conn.close()
    return redirect(url_for('user', user_id=user_id))


if __name__ == '__main__':
    app.run()
