import sys
import os
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from sankeyflow import Sankey
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import plotly.graph_objects as go
from api.airports import get_airports
from api.flight import get_flights
from api.planes import get_planes

# Charger les données des aéroports, des vols et des avions
airports_data = get_airports()
flights_data = get_flights()
planes_data = get_planes()

# Assurez-vous que les colonnes lat et lon sont bien des nombres, et gérez les erreurs
airports_data['lat'] = pd.to_numeric(airports_data['lat'], errors='coerce')
airports_data['lon'] = pd.to_numeric(airports_data['lon'], errors='coerce')

# Filtrer les lignes qui n'ont pas pu être converties en nombres
airports_data = airports_data.dropna(subset=['lat', 'lon'])

# Afficher les données dans Streamlit
st.title("Données des aéroports")
st.dataframe(airports_data)

# Créer une carte avec Folium et afficher les aéroports
m = folium.Map(location=[airports_data['lat'].mean(), airports_data['lon'].mean()], zoom_start=5)

for index, row in airports_data.iterrows():
    folium.Marker([row['lat'], row['lon']], popup=row['name']).add_to(m)

# Nombre total d'aéroports, de départ et de destination
st.header("Nombre total d'aéroports, de départ et de destination")
total_airports = len(airports_data['faa'].unique())
departure_airports = len(flights_data['origin'].unique())
destination_airports = len(flights_data['dest'].unique())
st.write(f"Total des aéroports : {total_airports}")
st.write(f"Aéroports de départ : {departure_airports}")
st.write(f"Aéroports de destination : {destination_airports}")

# Nombre d'aéroports aux États-Unis où on ne passe pas à l'heure d'été
st.header("Nombre d'aéroports aux États-Unis où on ne passe pas à l'heure d'été")
no_dst_airports = len(airports_data[airports_data['dst'] == 'N'])
st.write(f"Aéroports sans heure d'été : {no_dst_airports}")

# Nombre de fuseaux horaires
st.header("Nombre de fuseaux horaires")
timezones = len(airports_data['tzone'].unique())
st.write(f"Nombre de fuseaux horaires : {timezones}")

# Nombre de vols annulés
st.header("Nombre de vols annulés")
cancelled_flights = len(flights_data[(flights_data['air_time'].isnull()) & (flights_data['arr_time'].isnull())])
st.write(f"Nombre de vols annulés : {cancelled_flights}")

# Aéroport de départ le plus emprunté
st.header("Aéroport de départ le plus emprunté")
most_used_departure_airport = flights_data['origin'].value_counts().idxmax()
st.write(f"Aéroport de départ le plus emprunté : {most_used_departure_airport}")

# Les 10 destinations les plus (moins) prisées
st.header("Les 10 destinations les plus prisées")
top_10_destinations = flights_data['dest'].value_counts().head(10)
st.bar_chart(top_10_destinations)

st.header("Les 10 destinations les moins prisées")
bottom_10_destinations = flights_data['dest'].value_counts().tail(10)
st.bar_chart(bottom_10_destinations)

# Les 10 avions qui ont le plus (moins) décollé
st.header("Les 10 avions qui ont le plus décollé")
top_10_planes = flights_data['tailnum'].value_counts().head(10)
st.bar_chart(top_10_planes)

st.header("Les 10 avions qui ont le moins décollé")
bottom_10_planes = flights_data['tailnum'].value_counts().tail(10)
st.dataframe(bottom_10_planes)

# Nombre de destinations desservies par chaque compagnie
st.header("Nombre de destinations desservies par chaque compagnie")
destinations_per_company = flights_data.groupby('carrier')['dest'].nunique()
st.bar_chart(destinations_per_company)

# Nombre de destinations desservies par chaque compagnie par aéroport d'origine
st.header("Nombre de destinations desservies par chaque compagnie par aéroport d'origine")
destinations_per_company_origin = flights_data.groupby(['carrier', 'origin'])['dest'].nunique().unstack().fillna(0)
st.dataframe(destinations_per_company_origin)

# Nombre de vols partant des aéroports de NYC vers Seattle, nombre de compagnies desservant cette destination, et nombre d'avions uniques
st.header("Vols de NYC vers Seattle")
nyc_to_seattle_flights = flights_data[(flights_data['origin'].isin(['JFK', 'LGA', 'EWR'])) & (flights_data['dest'] == 'SEA')]
num_nyc_to_seattle_flights = len(nyc_to_seattle_flights)
num_companies_to_seattle = nyc_to_seattle_flights['carrier'].nunique()
num_unique_planes_to_seattle = nyc_to_seattle_flights['tailnum'].nunique()
st.write(f"Nombre de vols de NYC vers Seattle : {num_nyc_to_seattle_flights}")
st.write(f"Nombre de compagnies desservant Seattle : {num_companies_to_seattle}")
st.write(f"Nombre d'avions uniques vers Seattle : {num_unique_planes_to_seattle}")

# Nombre de vols par destination
st.header("Nombre de vols par destination")
flights_per_destination = flights_data['dest'].value_counts()
st.bar_chart(flights_per_destination)

# Tri des vols par destination, aéroport d'origine, compagnie
st.header("Tri des vols par destination, aéroport d'origine, compagnie")
sorted_flights = flights_data.sort_values(by=['dest', 'origin', 'carrier'])
st.dataframe(sorted_flights)

# Compagnies qui n'opèrent pas sur tous les aéroports d'origine
st.header("Compagnies qui n'opèrent pas sur tous les aéroports d'origine")
all_origins = flights_data['origin'].unique()
companies_not_all_origins = flights_data.groupby('carrier')['origin'].nunique().loc[lambda x: x < len(all_origins)]
st.dataframe(companies_not_all_origins)

# Compagnies qui desservent l'ensemble des destinations
st.header("Compagnies qui desservent l'ensemble des destinations")
all_destinations = flights_data['dest'].unique()
companies_all_destinations = flights_data.groupby('carrier')['dest'].nunique().loc[lambda x: x == len(all_destinations)]
st.dataframe(companies_all_destinations)

# Tableau des origines et des destinations pour l'ensemble des compagnies
# Regroupement des données par compagnie, origine, destination
origins_destinations_per_company = flights_data.groupby(['carrier', 'origin', 'dest']).size().unstack().fillna(0)

# Affichage du tableau dans Streamlit
st.header("Tableau des origines et des destinations pour l'ensemble des compagnies")
st.dataframe(origins_destinations_per_company)

# Préparation des données pour le diagramme de flux (Sankey)
all_origins = flights_data['origin'].unique()
all_destinations = flights_data['dest'].unique()

# Combinaison de toutes les villes (origines et destinations)
all_locations = list(set(all_origins) | set(all_destinations))

# Création des indices pour les villes
location_indices = {location: i for i, location in enumerate(all_locations)}

# Création des flux pour le Sankey
sources = [location_indices[origin] for origin in flights_data['origin']]
targets = [location_indices[dest] for dest in flights_data['dest']]
values = flights_data.groupby(['origin', 'dest']).size().tolist()

# Création du diagramme Sankey
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_locations,  # Utilisation de toutes les villes (origines et destinations)
        color="blue"
    ),
    link=dict(
        source=sources,  # Indices des villes d'origine
        target=targets,  # Indices des villes de destination
        value=values,    # Quantité de vols entre origine et destination
        color="rgba(31, 119, 180, 0.8)"
    )
))

# Configuration du layout
fig.update_layout(title_text="Diagramme de flux des vols entre les villes par compagnie", font_size=10)

# Affichage du diagramme dans Streamlit
st.plotly_chart(fig)

# Destinations exclusives à certaines compagnies
st.header("Destinations exclusives à certaines compagnies")
exclusive_destinations = flights_data.groupby('dest')['carrier'].nunique().loc[lambda x: x == 1]
st.dataframe(exclusive_destinations)

# Filtrer le vol pour trouver ceux exploités par United, American ou Delta
st.header("Vols exploités par United, American ou Delta")
filtered_flights = flights_data[flights_data['carrier'].isin(['UA', 'AA', 'DL'])]
st.dataframe(filtered_flights)

# Afficher la carte dans Streamlit
st.title("Carte des aéroports")
st_folium(m)