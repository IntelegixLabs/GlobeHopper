# Importing Lib for Python works and Flasks
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_cors import CORS

# Importing Supporting Lib
import APP_Constants
# importing the API blueprints
from api.globehopper_api import globehopper_Blueprint
from api.hotels.hotels_api import hotel_blp
from api.tbo.tbo_api import tbo_blp

app = Flask(__name__)
CORS(app)

app.register_blueprint(blueprint=globehopper_Blueprint, url_prefix=APP_Constants.APP_ENDPOINT)
app.register_blueprint(blueprint=hotel_blp, url_prefix=APP_Constants.APP_ENDPOINT)
app.register_blueprint(blueprint=tbo_blp, url_prefix=APP_Constants.APP_ENDPOINT)

rth = logging.handlers.RotatingFileHandler(
    filename='./logs/globehopper.log',
    maxBytes=25000,
    backupCount=10
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s  : %(message)s', handlers=[rth])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
