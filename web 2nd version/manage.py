from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app,db
from exts import db
from app.models import *

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
@manager.command
def create_db():
    db.create_all()
if __name__ == "__main__":
    manager.run()