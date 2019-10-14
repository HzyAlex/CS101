from flask import Flask
import random


app = Flask(__name__)


@app.route('/pre/<t1>/<t2>')
def pre(t1, t2):
    return str(random.random())


if __name__ == '__main__':
    app.run()
