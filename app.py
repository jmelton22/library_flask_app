from flask import Flask, render_template
from config import Config
import pymysql

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def main():
    connection = pymysql.connect(host=app.config['HOSTNAME'],
                                 user=app.config['USERNAME'],
                                 password=app.config['PASSWORD'],
                                 db=app.config['DATABASE'],
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            query = 'SELECT * FROM flask_test.test_tbl'
            cursor.execute(query)
            result = cursor.fetchall()
            return render_template('main.html', test=result)

    except Exception as e:
        print(e)
    finally:
        connection.close()


if __name__ == '__main__':
    app.run()
