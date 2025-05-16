#!/usr/bin/env python3

import mysql.connector
import csv
import uuid

# Connect to MySQL server (without database)
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password'  # Replace with your actual MySQL root password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create ALX_prodev database if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

# Connect specifically to ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',  # Replace with your actual MySQL root password
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create user_data table
def create_table(connection):
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX(user_id)
    )
    """
    cursor.execute(query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

# Insert data from CSV file
def insert_data(connection, filename):
    cursor = connection.cursor()
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check if user already exists
            cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (row['user_id'],))
            if cursor.fetchone():
                continue
            query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                row['user_id'],
                row['name'],
                row['email'],
                row['age']
            ))
    connection.commit()
    cursor.close()
