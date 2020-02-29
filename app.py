from flask import Flask
from config import Config
import pymysql

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def test():
    connection = pymysql.connect(host=app.config['HOSTNAME'],
                                 user=app.config['USERNAME'],
                                 password=app.config['PASSWORD'],
                                 db=app.config['DATABASE'])

    try:
        with connection.cursor() as cursor:
            query = 'SELECT * FROM flask_test.test_tbl'
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            return result

    except Exception as e:
        print(e)
    finally:
        connection.close()


if __name__ == '__main__':
    app.run()
