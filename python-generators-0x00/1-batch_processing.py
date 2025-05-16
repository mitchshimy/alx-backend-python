# --- Mock User Database ---
# This list simulates a user database.
# For demonstration, ages cycle to test filtering.
mock_users_database = [
    {'id': i, 'name': f'User{i}', 'age': 20 + ((i-1) % 20)} # Ages 20-39 repeating
    for i in range(1, 51) # 50 mock users
]

# --- Function to stream users in batches (Generator) ---
def stream_users_in_batches(batch_size):
    """
    Generator function to fetch users from the mock database in batches.
    It uses 'yield' to produce one batch at a time, making it memory-efficient.

    Args:
        batch_size (int): The number of user records per batch. Must be positive.

    Yields:
        list: A batch (list) of user dictionaries.
    """
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer.")

    # Loop 1: Iterating through the database to create and yield batches.
    for i in range(0, len(mock_users_database), batch_size):
        batch = mock_users_database[i:i + batch_size]
        yield batch

# --- Function to process batches ---
def batch_processing(batch_size):
    """
    Processes batches of users from stream_users_in_batches to filter
    users who are older than 25.

    Args:
        batch_size (int): The size of batches to retrieve and process.

    Returns:
        list: A list of user dictionaries for users older than 25.
    """
    users_over_25 = []

    # Loop 2: Iterating through batches from the stream_users_in_batches generator.
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Iterating through users within the current batch for filtering.
        for user in batch:
            if user['age'] > 25:
                users_over_25.append(user)
                
    return users_over_25
