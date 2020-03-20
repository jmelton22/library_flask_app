from flask import Flask, render_template
from config import Config
import pymysql

app = Flask(__name__)
app.config.from_object(Config)

# TODO: Set up models for database objects?


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books')
def books():
    connection = pymysql.connect(host=app.config['HOSTNAME'],
                                 user=app.config['USERNAME'],
                                 password=app.config['PASSWORD'],
                                 db=app.config['DATABASE'],
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            query = (
                'SELECT * '
                'FROM book '
                'JOIN author '
                'ON book.author=author.author_id'
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
    connection = pymysql.connect(host=app.config['HOSTNAME'],
                                 user=app.config['USERNAME'],
                                 password=app.config['PASSWORD'],
                                 db=app.config['DATABASE'],
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            query = (
                'SELECT * '
                'FROM book '
                'JOIN author '
                'ON book.author=author.author_id '
                f'WHERE book.book_id={book_id}'
            )
            cursor.execute(query)
            result = cursor.fetchall()
            return render_template('book.html', book=result[0])

    except Exception as e:
        print(e)
    finally:
        connection.close()


@app.route('/author/<author_id>')
def author(author_id):
    pass


if __name__ == '__main__':
    app.run()
