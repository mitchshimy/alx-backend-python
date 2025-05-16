# --- Simulated User Database Table ---
# This list simulates a table, which we'll conceptually call 'user_data_table'.
# In a real-world application, this data would typically be fetched from an actual database.
user_data_table = [
    {'id': i, 'name': f'User{i}', 'age': 20 + ((i-1) % 20)} # Ages cycle from 20 to 39
    for i in range(1, 51) # Create 50 mock user records
]

# --- Function to stream users in batches (Generator) ---
def stream_users_in_batches(batch_size):
    """
    Generator function to fetch rows in batches from the 'user_data_table'.
    This simulates fetching data from a database table like 'user_data'
    in chunks, using 'yield' for memory efficiency. A conceptual SQL query
    for each batch might be "SELECT * FROM user_data LIMIT batch_size OFFSET current_offset;".

    Args:
        batch_size (int): The number of user records (rows) to include in each batch.
                          Must be a positive integer.

    Yields:
        list: A batch, which is a list of user dictionaries (rows).
    """
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer.")

    # Loop 1: Iterating through the 'user_data_table' to create and yield batches.
    # This loop simulates fetching data page by page or batch by batch.
    for i in range(0, len(user_data_table), batch_size):
        # The slicing below simulates fetching a specific batch of records.
        # For example, the first batch is like "SELECT * FROM user_data LIMIT batch_size OFFSET 0;"
        # The second is like "SELECT * FROM user_data LIMIT batch_size OFFSET batch_size;" and so on.
        batch = user_data_table[i:i + batch_size]
        yield batch

# --- Function to process batches ---
def batch_processing(batch_size):
    """
    Processes batches of user records obtained from stream_users_in_batches.
    It filters these records to find users who are older than 25.

    Args:
        batch_size (int): The size of batches to retrieve from the stream
                          and then process.

    Returns:
        list: A list containing all user dictionaries for users over the age of 25.
              This is the result of processing (filtering) the 'user_data_table'.
    """
    users_over_25 = []

    # Loop 2: Iterating through the batches provided by the stream_users_in_batches generator.
    # Each 'batch' here represents a chunk of rows from 'user_data_table'.
    for batch in stream_users_in_batches(batch_size):
        
        # Loop 3: Iterating through individual user records within the current batch.
        for user_record in batch: # Each 'user_record' is like a row from a SELECT query
            if user_record['age'] > 25:
                users_over_25.append(user_record)
                
    return users_over_25
