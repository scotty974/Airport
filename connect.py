import psycopg2
import json

def connect_to_db():
    try:
        db_params = {
            'host': '52.47.102.168',
            'port': '5432',
            'dbname': 'airport',
            'user': 'postgres',
            'password': '123'
        }

        # Loguer les paramètres pour vérifier leur contenu
        print(json.dumps(db_params, ensure_ascii=False, indent=4))

        conn = psycopg2.connect(**db_params)
        print("Connexion réussie")
        return conn

    except psycopg2.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

connect_to_db()
