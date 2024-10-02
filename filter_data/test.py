import pandas as pd
from connect import connect_to_db

# Connect to the database
conn = connect_to_db()
cur = conn.cursor()

# Check if the table exists
cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'airports')")
table_exists = cur.fetchone()[0]

if table_exists:
    print("The table 'airports' already exists in the database.")
    # Fetch the first 5 rows from the 'airports' table
    cur.execute("SELECT * FROM airports LIMIT 5")
    rows = cur.fetchall()

    # Print the first 5 rows
    for row in rows:
        print(row)