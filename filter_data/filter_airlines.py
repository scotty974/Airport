import pandas as pd
from connect import connect_to_db
def read_data():  
    try:
        # recupération des données
        airlines_data = pd.read_json('data/airlines.json')

        # filtre des données
        # on drop si il y a des nuls
        airlines_data.dropna(inplace=True)

        print(airlines_data.head())
        return airlines_data
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def insert_data(data):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        for index, row in data.iterrows():
            cursor.execute("INSERT INTO airlines VALUES (%s, %s)", (row['carrier'], row['name']))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        
if __name__ == '__main__':
    conn = connect_to_db()
    data = read_data()
    insert_data(data)
    
    if conn and not data.empty:
        insert_data(data)
        conn.close()