import logging
import os
import sqlite3
import sys

module_directory = os.path.dirname(os.path.realpath(__file__))

print(module_directory)


def connection():
    try:
        return sqlite3.connect(module_directory + "/dimon.db")
    except Exception as e:
        logging.error("Failed to connect database: %s", e)
        return False


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def select_query(query, data=None):
    """Select Operation."""
    try:
        db = connection()
        db.row_factory = dict_factory
        cursor = db.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        return cursor.fetchall()

    except Exception as e:
        logging.error("Failed select query: %s", e)
        return None


def select_one_query(query, data=None):
    try:
        db = connection()
        db.row_factory = dict_factory
        cursor = db.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        return cursor.fetchone()

    except Exception as e:
        logging.error("Failed select one query: %s", e)
        return None


def query_execute(query, data=None):
    """CRUD Operation."""
    try:
        db = connection()
        cur = db.cursor()
        if data:
            cur.execute(query, data)
        else:
            cur.execute(query)
        db.commit()
        return True

    except Exception as e:
        logging.error("Failed execute query: %s", e)
        return False


if __name__ == '__main__':
    connection()
