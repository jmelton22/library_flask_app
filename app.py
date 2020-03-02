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
            return result

    except Exception as e:
        print(e)
    finally:
        connection.close()


if __name__ == '__main__':
    app.run()
