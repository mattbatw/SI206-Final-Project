import sqlite3
import os

def connect_to_database(db_filename):
    """
    Connects to the database.

    Parameters
    -----------------------
    db_filename: string
        The database file to use.

    Returns
    -----------------------
    cur: Cursor
        The database cursor object.

    conn: Connection
        The database connection object.
    """

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_filename)
    cur = conn.cursor()
    return cur, conn



