import requests
import sqlite3

def fetch_open_meteo_data(latitude, longitude, start_date, end_date):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto",
        # "hourly": "temperature_2m",
        "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum",
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        # print("Error code 200")
        return response.json()
    
    else:
        print(f"Error fetching data from Open-Meteo API. Status code: {response.status_code}")
        print(response.text)
        return None


def insert_country(connection, name, timezone):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO countries (name, timezone) VALUES (?, ?)", (name, timezone))
    connection.commit()
    return cursor.lastrowid

def insert_city(connection, name, longitude, latitude, country_id):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO cities (name, longitude, latitude, country_id) VALUES (?, ?, ?, ?)", (name, longitude, latitude, country_id))
    connection.commit()
    return cursor.lastrowid

def insert_daily_weather_entry(connection, date, min_temp, max_temp, mean_temp, precipitation, city_id):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO daily_weather_entries (date, min_temp, max_temp, mean_temp, precipitation, city_id) "
                   "VALUES (?, ?, ?, ?, ?, ?)", (date, min_temp, max_temp, mean_temp, precipitation, city_id))
    connection.commit()
    return cursor.lastrowid

def update_database(connection, latitude, longitude, start_date, end_date):
    open_meteo_data = fetch_open_meteo_data(latitude, longitude, start_date, end_date)

    if not open_meteo_data:
        print("Failed to fetch data from Open-Meteo API. Database not updated.")
        return

    # Insert or update countries and cities (assuming a country and city for the given latitude and longitude)
    country_id = insert_country(connection, "Germany", "CET")
    city_id = insert_city(connection, "Berlin", float(longitude), float(latitude), country_id)

    # Insert daily weather entries
    for i in range(len(open_meteo_data['daily']['time'])):
        date = open_meteo_data['daily']['time'][i]
        min_temp = open_meteo_data['daily']['temperature_2m_min'][i]
        max_temp = open_meteo_data['daily']['temperature_2m_max'][i]
        mean_temp = open_meteo_data['daily']['temperature_2m_mean'][i]
        precipitation = open_meteo_data['daily']['precipitation_sum'][i]

        # Insert or update daily weather entry
        insert_daily_weather_entry(connection, date, min_temp, max_temp, mean_temp, precipitation, city_id)

    print("Database updated successfully.")

database_path = "db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db"

# Connect to SQLite database
connection = sqlite3.connect(database_path)

latitude = "52.52"
longitude = "13.419"
start_date = "2023-12-01"
end_date = "2023-12-07"

# Fetch data from Open Meteo API
open_meteo_data = fetch_open_meteo_data(latitude, longitude, start_date, end_date)

# Insert data into SQLite database
# insert_data_into_database(connection, open_meteo_data)

update_database(connection, latitude, longitude, start_date, end_date)
# Close the database connection
connection.close()

print(open_meteo_data)
