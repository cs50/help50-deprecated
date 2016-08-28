from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import flask_migrate
import os
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://" + os.environ["MYSQL_USERNAME"] + ":" + os.environ["MYSQL_PASSWORD"] + "@" + os.environ["MYSQL_HOST"] + "/" + os.environ["MYSQL_DATABASE"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Input(db.Model):
    __tablename__ = "inputs"
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    cmd = db.Column(db.String(length=1024), nullable=True)
    script = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(length=32), nullable=True, index=True)
    created = db.Column(db.DateTime, default=func.now(), index=True)

class Output(db.Model):
    __tablename__ = "outputs"
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    input_id = db.Column(db.BigInteger, db.ForeignKey("inputs.id"))
    output = db.Column(db.Text)

if __name__ == '__main__':
    manager.run()