# config.py

import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import urllib.parse

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

server ="localhost"
database = "TrailTest"
username = "SA"
driver = "ODBC+Driver+17+for+SQL+Server"
password = "C0mp2001!"

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mssql+pyodbc://{username}:{urllib.parse.quote_plus(password)}@{server}/{database}"
    f"?driver={driver}"
    '&Encrypt=yes'
    '&TrustServerCertificate=Yes'
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)