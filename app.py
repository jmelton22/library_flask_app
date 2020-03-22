from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from config import Config
from forms import LoginForm, RegisterForm
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

Author = Base.classes.author
Book = Base.classes.book
User = Base.classes.user


def connect_to_db():
    return pymysql.connect(host=app.config['HOSTNAME'],
                           user=app.config['USERNAME'],
                           password=app.config['PASSWORD'],
                           db=app.config['DATABASE'],
                           cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html', title='Sign Up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/user/<user_id>')
def user(user_id):
    pass


@app.route('/books')
def books():
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            query = (
                'SELECT * '
                'FROM book '
                'JOIN author '
                'USING (author_id)'
            )
            cursor.execute(query)
            result = cursor.fetchall()
            return render_template('books.html', books=result)

    except Exception as e:
        print(e)
    finally:
        connection.close()


@app.route('/book/<book_id>')
def book(book_id):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            query = (
                'SELECT * '
                'FROM book '
                'JOIN author '
                'USING (author_id)'
                f'WHERE book.book_id={book_id}'
            )
            cursor.execute(query)
            result = cursor.fetchone()
            return render_template('book.html', book=result)

    except Exception as e:
        print(e)
    finally:
        connection.close()


@app.route('/author/<author_id>')
def author(author_id):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            query = (
                'SELECT * '
                'FROM author '
                f'WHERE author_id={author_id}'
            )
            cursor.execute(query)
            result_author = cursor.fetchone()

            query = (
                'SELECT * '
                'FROM book '
                f'WHERE book.author_id={author_id}'
            )
            cursor.execute(query)
            result_books = cursor.fetchall()
            return render_template('author.html', author=result_author, books=result_books)

    except Exception as e:
        print(e)
    finally:
        connection.close()


if __name__ == '__main__':
    app.run()
