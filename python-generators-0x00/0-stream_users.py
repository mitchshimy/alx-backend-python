#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator that yields one user row at a time as a dictionary"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # Replace with your actual MySQL root password
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
