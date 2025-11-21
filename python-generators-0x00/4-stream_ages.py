#!/usr/bin/python3
"""
4-stream_ages.py - Compute average age using a generator
"""

import mysql.connector
from mysql.connector import Error
seed = __import__('seed')


def stream_user_ages():
    """
    Generator that yields ages of users one by one
    """
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")

        for row in cursor:  # Loop 1: stream one age at a time
            yield row["age"]

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error: {e}")


def compute_average_age():
    """
    Compute average age using the stream_user_ages generator
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 2: iterate ages
        total_age += age
        count += 1

    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    compute_average_age()
