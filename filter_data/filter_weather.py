import pandas as pd
from connect import connect_to_db

def read_data():
    try:
        # Load the data
        weather = pd.read_excel('data/weather.xlsx', engine='openpyxl')

        weather_split = weather['origin,year,month,day,hour,temp,dewp,humid,wind_dir,wind_speed,wind_gust,precip,pressure,visib,time_hour'].str.split(',', expand=True)

        weather_split.columns = ['origin', 'year', 'month', 'day', 'hour', 'temp', 'dewp', 'humid', 'wind_dir', 'wind_speed', 'wind_gust', 'precip', 'pressure', 'visib', 'time_hour']

        print(weather_split.head())
        return weather_split
    except Exception as e:
        print(f"An error occurred: {e}")

def insert_data(data):
    try:
        # Connect to the database
        conn = connect_to_db()
        cur = conn.cursor()

        # Check if the table exists
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'weather')")
        table_exists = cur.fetchone()[0]

        if table_exists:
            print("The table 'weather' already exists in the database.")
        else:
            print("The table 'weather' does not exist in the database.")
            # Create the table
            cur.execute("""
            CREATE TABLE weather (
                origin VARCHAR,
                year INT,
                month INT,
                day INT,
                hour INT,
                temp FLOAT,
                dewp FLOAT,
                humid FLOAT,
                wind_dir FLOAT,
                wind_speed FLOAT,
                wind_gust FLOAT,
                precip FLOAT,
                pressure FLOAT,
                visib FLOAT,
                time_hour VARCHAR
            )
            """)
            print("Table 'weather' created successfully.")
            
        # Insert data into the database
        for index, row in data.iterrows():
            cur.execute("""
            INSERT INTO weather (origin, year, month, day, hour, temp, dewp, humid, wind_dir, wind_speed, wind_gust, precip, pressure, visib, time_hour)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['origin'], 
                int(row['year']) if row['year'] and row['year'].strip() else None,
                int(row['month']) if row['month'] and row['month'].strip() else None,
                int(row['day']) if row['day'] and row['day'].strip() else None,
                int(row['hour']) if row['hour'] and row['hour'].strip() else None,
                float(row['temp']) if row['temp'] and row['temp'].strip() else None,
                float(row['dewp']) if row['dewp'] and row['dewp'].strip() else None,
                float(row['humid']) if row['humid'] and row['humid'].strip() else None,
                float(row['wind_dir']) if row['wind_dir'] and row['wind_dir'].strip() else None,
                float(row['wind_speed']) if row['wind_speed'] and row['wind_speed'].strip() else None,
                float(row['wind_gust']) if row['wind_gust'] and row['wind_gust'].strip() else None,
                float(row['precip']) if row['precip'] and row['precip'].strip() else None,
                float(row['pressure']) if row['pressure'] and row['pressure'].strip() else None,
                float(row['visib']) if row['visib'] and row['visib'].strip() else None,
                row['time_hour']
            ))

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