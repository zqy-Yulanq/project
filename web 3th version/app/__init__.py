import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
import config
from exts import db
pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app=app)
handler = logging.FileHandler('log/flask.log', encoding='UTF-8')
handler.setLevel(logging.DEBUG)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)
from app import views

