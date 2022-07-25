import time
import random

from flask import Flask

app = Flask(__name__)
error_codes = ('404', '502')

@app.route('/one')
def route_one():
    time.sleep(random.random() * 0.2)
    return 'Route 1\n'

@app.route('/two')
def route_two():
    time.sleep(random.random() * 0.2)
    return 'Route 2\n'

@app.route('/three')
def route_three():
    time.sleep(random.random() * 0.2)
    return 'Route 3\n'

@app.route('/four')
def route_four():
    time.sleep(random.random() * 0.2)
    return 'Error...\n', random.choice(error_codes)



if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)