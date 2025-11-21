#!/usr/bin/python3
"""
0-stream_users.py - generator to stream rows from user_data table
"""

import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that yields rows from the user_data table one by one"""
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bondeni001.",  # update your MySQL password
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)  # get rows as dicts
        cursor.execute("SELECT * FROM user_data")

        # Single loop: yield one row at a time
        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error connecting to database: {e}")
