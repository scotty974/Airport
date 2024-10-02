import pandas as pd
from db.connect import connect_to_db
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
        # check if the table exists
        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'airlines')")
        table_exists = cursor.fetchone()[0]

        if table_exists:
            print("The table 'airlines' already exists in the database.")
        else:
            print("The table 'airlines' does not exist in the database.")
            cursor.execute("CREATE TABLE airlines (carrier VARCHAR PRIMARY KEY, name VARCHAR)")
        
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