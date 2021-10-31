from flask import Flask, redirect
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def homepage():    
  return redirect("https://github.com/ading2210/Hypixel-Discord-Bot", code=302)

@app.route("/static/<path:path>")
def serveStaticFile(path):
  return send_from_directory("static", path)

if __name__ == "__main__":
  app.run(host="0.0.0.0")