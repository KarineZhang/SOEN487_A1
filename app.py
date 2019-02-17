from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy

# need an app before we import models because models need it
app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
db.init_app(app)
