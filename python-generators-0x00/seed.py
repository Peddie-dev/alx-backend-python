#!/usr/bin/python3
"""
seed.py - Creates ALX_prodev database, user_data table,
and inserts data from user_data.csv
"""

import mysql.connector
from mysql.connector import Error
import csv


# -----------------------------------------------------------
# 1. Connect to MySQL server (NO database selected yet)
# -----------------------------------------------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""    # add password if you have one
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# -----------------------------------------------------------
# 2. Create ALX_prodev database if it doesn't exist
# -----------------------------------------------------------
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


# -----------------------------------------------------------
# 3. Connect directly to ALX_prodev database
# -----------------------------------------------------------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   # add password if needed
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


# -----------------------------------------------------------
# 4. Create user_data table if it does not exist
# -----------------------------------------------------------
def create_table(connection):
    try:
        query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(10,2) NOT NULL
        );
        """
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


# -----------------------------------------------------------
# 5. Insert data from CSV file into user_data table
# -----------------------------------------------------------
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()

        with open(csv_file, "r", newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute(
                    """
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (row["user_id"], row["name"], row["email"], row["age"])
                )

        connection.commit()
        cursor.close()
        print("Data inserted successfully")

    except Error as e:
        print(f"Error inserting data: {e}")

    except FileNotFoundError:
        print(f"CSV file not found: {csv_file}")

