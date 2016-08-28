import MySQLdb as mdb
import os
from warnings import filterwarnings

# establish connection to database
con = mdb.connect(
    os.environ['MYSQL_HOST'],
    os.environ['MYSQL_USER'],
    os.environ['MYSQL_PASS'],
    os.environ['MYSQL_DATABASE'],
    charset='utf8'
)
cur = con.cursor()

# disable 'table already exists' warnings
filterwarnings('ignore', category=mdb.Warning)

def configure():
    inputs_schema = '''
    CREATE TABLE IF NOT EXISTS inputs (
        id BIGINT NOT NULL AUTO_INCREMENT,
        cmd VARCHAR(1024) NULL,
        script TEXT NOT NULL,
        username VARCHAR(32) NULL,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB;
    '''
    
    outputs_schema = '''
    CREATE TABLE IF NOT EXISTS outputs (
        id BIGINT NOT NULL AUTO_INCREMENT,
        input_id BIGINT,
        output TEXT,
        PRIMARY KEY (id),
        FOREIGN KEY (input_id) REFERENCES inputs(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    '''
    
    cur.execute(inputs_schema)
    cur.execute(outputs_schema)

def insert_io(cmd, script, output):
    inputstatement = (
        "INSERT INTO inputs (cmd, script)"
        "VALUES (%s, %s)"
    )
    inputdata = (cmd, script)
    cur.execute(inputstatement, inputdata)
        
    # check to make sure insert was successful before continuing
    if cur.rowcount == 1:
        # if there is an output,insert
        if output is not None:
            outputstatement = (
                "INSERT INTO outputs(input_id, output)"
                "VALUES (LAST_INSERT_ID(), %s)"
            )
            outputdata =(output,)
            cur.execute(outputstatement, outputdata)
        con.commit()


    
