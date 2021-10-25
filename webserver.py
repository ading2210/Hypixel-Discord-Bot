from flask import Flask
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def hello_world():    
  return '[placeholder]'

@app.route("/static/<path:path>")
def serveStaticFile(path):
  return send_from_directory("static", path)

if __name__ == "__main__":
  app.run(host="0.0.0.0")