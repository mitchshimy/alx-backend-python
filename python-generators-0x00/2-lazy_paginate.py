#!/usr/bin/python3
import mysql.connector
import os

def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database using LIMIT and OFFSET.

    Args:
        page_size (int): Number of users to fetch.
        offset (int): Offset to start fetching from.

    Returns:
        list: List of user dicts.
    """
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def lazy_paginate(page_size):
    """
    Generator that lazily fetches pages of users from the database.

    Args:
        page_size (int): Number of users per page.

    Yields:
        list: Next batch of user dicts.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# For manual testing (optional)
if __name__ == "__main__":
    for i, page in enumerate(lazy_paginate(5), 1):
        print(f"Page {i}:")
        for user in page:
            print(user)
        print()
