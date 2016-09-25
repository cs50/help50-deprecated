from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from manage import Output, Input
from pytz import timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# http://stackoverflow.com/a/9157305
uri = "mysql://" + os.environ["MYSQL_USERNAME"] + ":" + os.environ["MYSQL_PASSWORD"] + "@" + os.environ["MYSQL_HOST"] + "/" + os.environ["MYSQL_DATABASE"] + "?charset=utf8"
engine = create_engine(uri)
Session = sessionmaker(bind=engine)
session = Session()

# logs input (and any helpful output)
def log(cmd, username, script, output):
    output_id = None
    if (output):
        help_out = Output(output=output)
        session.add(help_out)
        session.commit()
        output_id = help_out.id
    help_in = Input(cmd=cmd, username=username, script=script, output_id=output_id, created=datetime.utcnow())
    session.add(help_in)
    try:
        session.commit()
    except:
        session.rollback()
        raise

# gets unreviewed inputs with no output
def unreviewed_matchless():
    return session.query(Input).filter(Input.output_id==None, Input.reviewed==False).order_by(Input.created).all()

# mark an input as reviewed
def mark_reviewed(input_id):
    row = session.query(Input).filter(Input.id==input_id).first()
    if (row != None):
        row.reviewed = True
    try:
        session.commit()
    except:
        session.rollback()
        raise
