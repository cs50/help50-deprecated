from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from manage import Output, Input
from pytz import timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

uri = "mysql://" + os.environ["MYSQL_USERNAME"] + ":" + os.environ["MYSQL_PASSWORD"] + "@" + os.environ["MYSQL_HOST"] + "/" + os.environ["MYSQL_DATABASE"]
engine = create_engine(uri)
Session = sessionmaker(bind=engine)
session = Session()

# cleans text for db input
def clean(text):
    return text.replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201C", "\"").replace(u"\u201D", "\"").encode("latin-1", "ignore")

# logs input (and any helpful output)
def log(cmd, username, script, output):
    output_id = None
    if (output):
        help_out = Output(output=clean(output))
        session.add(help_out)
        session.commit()
        output_id = help_out.id
    help_in = Input(cmd=clean(cmd), username=clean(username), script=clean(script), output_id=output_id, created=datetime.utcnow())
    session.add(help_in)
    session.commit()

# gets unreviewed inputs with no output
def unreviewed_matchless():
    return session.query(Input).filter(Input.output_id==None, Input.reviewed==False).order_by(Input.created).all()

# mark an input as reviewed
def mark_reviewed(input_id):
    row = session.query(Input).filter(Input.id==input_id).first()
    if (row != None):
        row.reviewed = True
    session.commit()
