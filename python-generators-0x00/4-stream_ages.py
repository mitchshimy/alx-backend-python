#!/usr/bin/python3
import mysql.connector
import os

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    
    # Loop 1: Yield ages one by one
    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()

def calculate_average_age():
    """
    Uses the stream_user_ages generator to compute average age without loading all data at once.
    """
    total_age = 0
    count = 0
    
    # Loop 2: Iterate over yielded ages to calculate sum and count
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        print("No users found.")
        return
    
    average = total_age / count
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()
