# Utility functions

import sqlite3
import os
import json

# FOR TESTING, REMOVE WHEN DONE
def write_json(filename, dict): 
    file = open(filename, 'w')
    file.write(json.dumps(dict))
    file.close()

def connect_to_database(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_filename)
    cur = conn.cursor()
    return cur, conn



