from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.sql import func
import flask_migrate
import os
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://" + os.environ["MYSQL_USERNAME"] + ":" + os.environ["MYSQL_PASSWORD"] + "@" + os.environ["MYSQL_HOST"] + "/" + os.environ["MYSQL_DATABASE"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Output(db.Model):
    __tablename__ = "outputs"
    mysql_default_charset = "utf8",
    mysql_collate = "utf8_general_ci"
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    output = db.Column(db.Text)

class Input(db.Model):
    __tablename__ = "inputs"
    mysql_default_charset = "utf8",
    mysql_collate =  "utf8_general_ci"
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    cmd = db.Column(db.String(length=1024), nullable=True)
    _script = db.Column("script", db.Text, nullable=False)
    username = db.Column(db.String(length=32), nullable=True, index=True)
    created = db.Column(db.DateTime, default=func.now(), index=True)
    output_id = db.Column(db.BigInteger, db.ForeignKey("outputs.id"), nullable=True)
    reviewed = db.Column(db.Boolean, default=False, index=True)

    # getter, strips ANSI codes
    @property
    def script(self):
        return re.compile(r"\x1b[^m]*m").sub("", self._script)

    # setter, preserves ANSI codes
    @script.setter
    def script(self, script):
        self._script = script

if __name__ == '__main__':
    manager.run()
