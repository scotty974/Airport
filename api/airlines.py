import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify
import json
import pandas as pd
from db.connect import connect_to_db

def get_airlines():
    # Établir une connexion à la base de données
    conn = connect_to_db()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM airlines")
            airlines = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

    airlines_df = pd.DataFrame(airlines, columns=columns)

    # Convertir les résultats en format JSON
    print(airlines_df.head())

    # Retourner les données sous forme de DataFrame
    return airlines_df
get_airlines()