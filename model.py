from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz
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
    # we're going to group together all similar results
    counter = 0
    result_map = {}

    # grab all results from db
    results = session.query(Input).filter(Input.output_id==None, Input.reviewed==False).order_by(Input.created).all()

    for result in results:
        # initialize dict with first grouping if none exists
        if len(result_map.keys()) < 1:
            result_map[counter] = [result]
            counter += 1
        else:
            # for every fuzzy grouping we've created, do a fuzzy search on all entries
            for k in result_map.keys():

                # breaks out of this loop after enclosing loop if match was found
                found = False

                # check ratios from 80 to 40, step size of -10
                for val in range(90, 49, -10):
                    # the most valuable line is *usually* the second, so test that
                    lines = result.script.split('\n')
                    test_line = lines[1] if len(lines) > 1 else lines[0]

                    ratios = []

                    # split each script by newlines, taking the 1st as a heuristic usually (most info)
                    for x in result_map[k]:
                        k_lines = x.script.split('\n')
                        k_test_line = k_lines[1] if len(k_lines) > 1 else k_lines[0]
                        ratios.append(fuzz.ratio(test_line, k_lines))

                    avg_ratio = sum(ratios) / len(ratios)

                    # if our average ratio is below what we're checking, it's similar
                    if avg_ratio >= val:
                        result_map[k].append(result)
                        found = True
                        break

                if found:
                    break

            # create new grouping if we were unsuccessful
            result_map[counter] = [result]
            counter += 1

    # get all lists into one list we can sort it in reverse
    groupings_list = []
    for k in result_map.keys(): groupings_list.append(result_map[k])
    groupings_list_sorted = sorted(groupings_list, key=len)
    groupings_list_sorted.reverse()

    # return flattened list
    return [item for sublist in groupings_list_sorted for item in sublist]

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
