from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object('config')
app.static_folder = 'static'

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
