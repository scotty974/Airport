import pandas as pd

def read_data():
    try:
        # Load the data
        flights = pd.read_excel('data/flights.xlsx', engine='openpyxl')
        flights.dropna(inplace=True)
        flights_split = flights['year, month, day, dep_times, sched_dep_time,sched_arr_time,dep_delay, arr_delay, carrier, flight, tailnum, origin, dest, air_time, distance '].str.split(',', expand=True)
        print(flights.head())
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
read_data()