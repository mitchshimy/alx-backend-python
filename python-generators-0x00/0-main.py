#!/usr/bin/python3

import seed

# Step 1: Connect to MySQL server
connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print("Connection successful")

    # Step 2: Connect to ALX_prodev database
    connection = seed.connect_to_prodev()
    if connection:
        # Step 3: Create the table
        seed.create_table(connection)

        # Step 4: Insert data from CSV file
        seed.insert_data(connection, 'user_data.csv')

        # Step 5: Check if database exists and display sample rows
        cursor = connection.cursor()
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print("Database ALX_prodev is present")

        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)

        cursor.close()
        connection.close()
