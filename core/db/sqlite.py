import os
from sqlite3 import dbapi2 as sqlite
from core.constants import DBNAME


def connect_to_ddbb():
    connection = sqlite.connect(database=os.path.join(os.path.dirname(os.path.abspath(__file__)), DBNAME))
    create_ddbb_data(connection)
    return connection


def create_ddbb_data(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS project (
                        project_id TEXT NOT NULL,
                        start_date INTEGER NOT NULL,
                        proposal_manager TEXT DEFAULT NULL,
                        data_management_system TEXT DEFAULT NULL,
                        metadata_path TEXT DEFAULT NULL,
                        PRIMARY KEY(project_id));''')
    connection.commit()


def close_connection_to_ddbb(connection):
    connection.close()
