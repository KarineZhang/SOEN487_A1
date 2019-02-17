from flask import Flask
from config import DevConfig, TestConfig

import sys

app = Flask(__name__)
# Path is empty when executed from test
if len(sys.path[0].split('\\')) > 1:
    app.config.from_object(DevConfig)
else:
    app.config.from_object(TestConfig)
app.secret_key = '40018892'

from db import db


db.create_all()
db.session.commit()
