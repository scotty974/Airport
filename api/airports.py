import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify
import json
import pandas as pd

from db.connect import connect_to_db
def get_airports():
    # Établir une connexion à la base de données
    conn = connect_to_db()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM airports")
            airports = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

    airports_df = pd.DataFrame(airports, columns=columns)

    # Convertir les résultats en format JSON
    print(airports_df.head())

    # Retourner les données sous forme de DataFrame
    return airports_df
    #return jsonify(airports)
get_airports()