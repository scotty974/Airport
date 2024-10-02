import pandas as pd
from db.connect import connect_to_db
from filter_flights import read_flights_data

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

def read_lost_weather():
    try:
        # Get the weather data
        weather_data = read_data()
        flights = read_flights_data()

        # Vérifier si les colonnes nécessaires sont présentes dans les deux DataFrames
        required_columns = ['year', 'month', 'day', 'hour', 'origin']
        if all(col in flights.columns for col in required_columns) and all(col in weather_data.columns for col in required_columns):
            # Fusionner les deux DataFrames sur les colonnes 'year', 'month', 'day', 'hour', 'origin'
            merged_data = flights.merge(weather_data, on=required_columns, how='left', indicator=True)

            # Trouver les lignes qui sont présentes dans flights mais pas dans weather_data
            lost_weather = merged_data[merged_data['_merge'] == 'left_only'][required_columns]

            # Extraire la liste des données météorologiques manquantes
            lost_weather_list = lost_weather.drop_duplicates().values.tolist()

            print(f"Missing weather data: {lost_weather}")
            return lost_weather_list
        else:
            print("Les colonnes nécessaires ne sont pas présentes dans les deux DataFrames.")
            return []
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return []
    

def insert_lost_weather(data):
    try:
        # Connect to the database
        conn = connect_to_db()
        cur = conn.cursor()

        # Insert data into the database
        for row in data:
            cur.execute("""
            INSERT INTO weather (origin, year, month, day, hour)
            VALUES (%s, %s, %s, %s, %s)
            """, (
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            ))

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

# Exemple d'utilisation
if __name__ == '__main__':
    lost_weather = read_lost_weather()
    if lost_weather:
        insert_lost_weather(lost_weather)
        print(f"{len(lost_weather)} lignes insérées avec succès dans la table 'weather  '.")