import pandas as pd
from connect import connect_to_db

def read_data():  
    try:
        # Récupération des données
        planes_data = pd.read_excel('data/planes.xlsx', engine='openpyxl')
        planes_split = planes_data['tailnum,year,type,manufacturer,model,engines,seats,speed,engine'].str.split(',', expand=True)
        planes_split.columns = ['tailnum', 'year', 'type', 'manufacturer', 'model', 'engines', 'seats', 'speed', 'engine']
        print(planes_split.head())
        return planes_split
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def insert_data(data):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'planes')")
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print("La table 'planes' n'existe pas dans la base de données. Création de la table.")
            cursor.execute("CREATE TABLE planes (tailnum VARCHAR PRIMARY KEY, year INT, type VARCHAR, manufacturer VARCHAR, model VARCHAR, engines VARCHAR, seats INT, speed INT, engine VARCHAR)")

        for index, row in data.iterrows():
            # Récupération des valeurs de la ligne
            tailnum = row['tailnum']
            
            # Conversion des colonnes en valeurs appropriées
            try:
                year = int(row['year']) if row['year'].strip() else None  # Utilise None si la chaîne est vide
                seats = int(row['seats']) if row['seats'].strip() else None
                speed = int(row['speed']) if row['speed'].strip() else None
            except ValueError:
                print(f"Erreur de conversion des données pour la ligne {index}: {row}")
                continue  # Ignore la ligne en cas d'erreur

            type = row['type']
            manufacturer = row['manufacturer']
            model = row['model']
            engines = row['engines']
            engine = row['engine']

            # Insertion dans la table
            cursor.execute("INSERT INTO planes (tailnum, year, type, manufacturer, model, engines, seats, speed, engine) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                           (tailnum, year, type, manufacturer, model, engines, seats, speed, engine))
        
        # Commit des changements après toutes les insertions
        conn.commit()
        print(f"{len(data)} lignes insérées avec succès dans la table 'planes'.")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    finally:
        # Fermeture du curseur et de la connexion
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    data = read_data()
    if data is not None and not data.empty:
        insert_data(data)
