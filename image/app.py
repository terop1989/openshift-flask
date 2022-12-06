import random

from flask import Flask

app = Flask(__name__)
status_codes = ('200','404')

@app.route('/')
def route_root():
    return ('Status...', random.choice(status_codes))


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)