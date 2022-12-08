import logging, random
from flask import Flask

def get_stream_logger():
  log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

  sh = logging.StreamHandler()
  sh.setFormatter(logging.Formatter(log_format))
  sh.setLevel(logging.INFO)

  logger = logging.getLogger("example-app")
  logger.setLevel(logging.INFO)
  logger.addHandler(sh)
  return logger

app = Flask(__name__)
status_codes = [200, 404]
logger = get_stream_logger()

@app.route('/')
def route_root():
  status = random.choice(status_codes)
  logger.info("calling root route")
  return ('Status ' + str(status) + '\n', status)

if __name__ == '__main__':
  app.run('0.0.0.0', 5000, threaded=True)