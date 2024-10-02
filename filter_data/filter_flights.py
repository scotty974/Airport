import pandas as pd
from db.connect import connect_to_db

def read_flights_data():
    try:
        # Récupération des données
        flights_data = pd.read_excel('data/flights.xlsx', engine='openpyxl')  # Ajuste le chemin selon tes besoins
        flights_split = flights_data['year,month,day,dep_time,sched_dep_time,dep_delay,arr_time,sched_arr_time,arr_delay,carrier,flight,tailnum,origin,dest,air_time,distance,hour,minute,time_hour'].str.split(',', expand=True)
        flights_split.columns = [
            'year',
            'month',
            'day',
            'dep_time',
            'sched_dep_time',
            'dep_delay',
            'arr_time',
            'sched_arr_time',
            'arr_delay',
            'carrier',
            'flight',
            'tailnum',
            'origin',
            'dest',
            'air_time',
            'distance',
            'hour',
            'minute',
            'time_hour'
        ]
        print(flights_split.head())
        return flights_split
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture des données de vol : {e}")

def insert_data(data):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Check if the table exists
        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'flights')")
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print("La table 'flights' n'existe pas, création de la table.")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                flight_id SERIAL PRIMARY KEY,
                year VARCHAR(4),
                month INTEGER,
                day INTEGER,
                dep_time INTEGER,
                arr_time INTEGER,
                sched_dep_time INTEGER,
                sched_arr_time INTEGER,
                dep_delay INTEGER,
                arr_delay INTEGER,
                carrier VARCHAR(2),
                tailnum VARCHAR(10),
                flight INTEGER,
                origin VARCHAR(3),
                dest VARCHAR(3),
                air_time INTEGER,
                distance INTEGER,
                time_hour TIMESTAMP,
                FOREIGN KEY (carrier) REFERENCES airlines(carrier),
                FOREIGN KEY (tailnum) REFERENCES planes(tailnum),
                FOREIGN KEY (origin) REFERENCES airports(faa),
                FOREIGN KEY (dest) REFERENCES airports(faa)
            )
            """)

        for index, row in data.iterrows():
            try:
                # Insérer les données dans la table flights
                cursor.execute("""
                    INSERT INTO flights (year, month, day, dep_time, arr_time, sched_dep_time, sched_arr_time, dep_delay, arr_delay, carrier, tailnum, flight, origin, dest, air_time, distance, time_hour)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['year'],
                    row['month'],
                    row['day'],
                    row['dep_time'],
                    row['arr_time'],
                    row['sched_dep_time'],
                    row['sched_arr_time'],
                    row['dep_delay'],
                    row['arr_delay'],
                    row['carrier'],
                    row['tailnum'],
                    row['flight'],
                    row['origin'],
                    row['dest'],
                    row['air_time'],
                    row['distance'],
                    row['time_hour']
                ))

                # Commit chaque insertion
                conn.commit()

            except Exception as e:
                print(f"Erreur lors de l'insertion de la ligne {index} : {e}")
                conn.rollback()  # Annule la transaction actuelle

        cursor.close()
        conn.close()
        print("Données insérées avec succès.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'insertion des données : {e}")

if __name__ == '__main__':
    data = read_flights_data()
    if data is not None and not data.empty:
        insert_data(data)
