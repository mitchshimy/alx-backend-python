# Connect to MySQL with Python and Populate Table

## 🎯 Objectives

* Connect to a MySQL server using Python (`mysql-connector-python`)
* Create a database (`ALX_prodev`) if it doesn't exist
* Create a table (`user_data`) with the following schema:
    * `user_id`: UUID (Primary Key, Indexed)
    * `name`: String (NOT NULL)
    * `email`: String (NOT NULL)
    * `age`: Decimal (NOT NULL)
* Populate the table from a CSV file (`user_data.csv`)
* Use a generator to stream data one row at a time (future implementation)

## 🧰 Prerequisites

Ensure the following are installed on your system:

* Python 3.6+
* `mysql-connector-python` module

    ```bash
    pip install mysql-connector-python
    ```
* A running instance of MySQL (e.g., `mysql-server`)
* Access credentials to connect (e.g., `root` user)

## 🔐 Configuration

The script assumes default MySQL credentials:

* Host: localhost
* User: root
* Password: (empty)

You can edit these values in `seed.py`:

```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
```
## How to Run

### Step 1: Place all files in the same directory:

- `seed.py`
- `0-main.py`
- `user_data.csv` (Download from [this CSV link](user_data.csv))

### Step 2: Make `0-main.py` executable:

```bash
chmod +x 0-main.py
```

### Step 3: Run the script:

```bash
./0-main.py

or

```bash
python3 0-main.py
```

Expected Output:

```plaintext
Connection successful
Table user_data created successfully
Database ALX_prodev is present
[('UUID1', 'Name1', 'Email1', 25), ('UUID2', 'Name2', 'Email2', 30), ...]
```
