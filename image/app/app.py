import logging, random
from flask import Flask, render_template
from pythonjsonlogger import jsonlogger

app_name = "flask-app"

def get_stream_logger(logger_name):
  log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  json_formatter = jsonlogger.JsonFormatter(log_format)

  sh = logging.StreamHandler()
  sh.setFormatter(json_formatter)
  sh.setLevel(logging.INFO)

  logger = logging.getLogger(logger_name)
  logger.setLevel(logging.INFO)
  logger.addHandler(sh)
  return logger

app = Flask(__name__)
status_codes = [200, 404]
logger = get_stream_logger(app_name)
index_menu = ["Setup", "First Application", "Feedback"]

@app.route('/')
def index():
  return render_template('index.html', title="Flask Site Main Page", menu=index_menu)

@app.route('/health')
def health():
  status = random.choice(status_codes)
  logger.info({"message" : "calling root route"})
  return ('Status ' + str(status) + '\n', status)

if __name__ == '__main__':
  app.run('0.0.0.0', 5000, threaded=True)