from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create database and import table classes
db = SQLAlchemy(app)
from models import User, Book, Author


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(email=form.email.data, password=hashed_password)
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


@app.route('/books')
def books():
    result = db.session.query(Book, Author).join(Author).all()
    return render_template('books.html', books=result)


@app.route('/book/<book_id>')
def book(book_id):
    book, author = db.session.query(Book, Author).join(Author).filter(Book.book_id == book_id).one()
    return render_template('book.html', book=book, author=author)


@app.route('/author/<author_id>')
def author(author_id):
    author = db.session.query(Author).filter(Author.author_id == author_id).one()
    books = db.session.query(Book).filter(Book.author_id == author_id).all()
    return render_template('author.html', author=author, books=books)


if __name__ == '__main__':
    app.run()
