import MySQLdb as mdb
import os
from warnings import filterwarnings

# establish connection to database
con = mdb.connect(
    os.environ['MYSQL_HOST'],
    os.environ['MYSQL_USER'],
    os.environ['MYSQL_PASS'],
    os.environ['MYSQL_DATABASE']
)
cur = con.cursor()

# disable 'table already exists' warnings
filterwarnings('ignore', category=mdb.Warning)

def configure():
    inputs_schema = '''
    CREATE TABLE IF NOT EXISTS inputs (
        id BIGINT NOT NULL AUTO_INCREMENT,
        cmd TEXT,
        script TEXT NOT NULL,
        username VARCHAR(32),
        created DATETIME,
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
    
