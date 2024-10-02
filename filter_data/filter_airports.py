import pandas as pd
from connect import connect_to_db

def read_data():
    try:
        # Load the data
        airports = pd.read_excel('data/airports.xlsx', engine='openpyxl')

        airports_split = airports['faa,name,lat,lon,alt,tz,dst,tzone'].str.split(',', expand=True)

        airports_split.columns = ['faa', 'name', 'lat', 'lon', 'alt', 'tz', 'dst', 'tzone']

        print(airports_split.head())
        return airports_split
    except Exception as e:
        print(f"An error occurred: {e}")

def insert_data(data):
    try:
        # Connect to the database
        conn = connect_to_db()
        cur = conn.cursor()

        # Check if the table exists
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'airports')")
        table_exists = cur.fetchone()[0]

        if table_exists:
            print("The table 'airports' already exists in the database.")
        else:
            print("The table 'airports' does not exist in the database.")
            # Create the table
            cur.execute("CREATE TABLE airports (faa VARCHAR PRIMARY KEY, name VARCHAR, lat FLOAT, lon FLOAT, alt INT, tz INT, dst VARCHAR, tzone VARCHAR)")

        # Insert data into the database
        for index, row in data.iterrows():
            faa = row['faa']
            name = row['name']
            lat = row['lat']
            lon = row['lon']
            alt = row['alt']
            tz = row['tz']
            dst = row['dst']
            tzone = row['tzone']

            cur.execute("INSERT INTO airports (faa, name, lat, lon, alt, tz, dst, tzone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (faa, name, lat, lon, alt, tz, dst, tzone))

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    data = read_data()
    if not data.empty:
        insert_data(data)

