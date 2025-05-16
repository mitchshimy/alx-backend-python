# Mock database of users for simulation
mock_users_database = [
    {'id': i, 'name': f'User{i}', 'age': 20 + (i % 15)}  # Ages cycle 20 to 34
    for i in range(1, 51)  # 50 users total
]

def paginate_users(page_size, offset):
    """
    Simulates fetching a page of users from the database.

    Args:
        page_size (int): Number of users per page.
        offset (int): Starting index to fetch users from.

    Returns:
        list: A list of users for the current page.
    """
    return mock_users_database[offset:offset + page_size]

def lazy_paginate(page_size):
    """
    Generator that lazily loads pages of users from the database.

    Args:
        page_size (int): Number of users per page.

    Yields:
        list: Next page (batch) of users.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # No more data to fetch
            break
        yield page
        offset += page_size


# Example usage for testing
if __name__ == "__main__":
    page_size = 10

    for i, page in enumerate(lazy_paginate(page_size), 1):
        print(f"Page {i}: {page}\n")
