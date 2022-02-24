from config import SQLALCHEMY_DATABASE_URI
from exts import db
from app import db
import os.path
db.create_all()