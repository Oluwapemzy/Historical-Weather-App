import sqlite3


# Phase 1 - Starter
# 
# Note: Display all real/float numbers to 2 decimal places.

'''
Satisfactory
'''

def select_all_countries(connection):
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        # Define the query
        query = "SELECT * from [countries]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()
        cursor.row_factory =sqlite3.Row # returns rows as dictionaries

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        
        my_results = ""
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")
            my_results+= f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}\n"

    except sqlite3.OperationalError as ex:
        print(ex)

    return my_results


def select_all_cities(connection):
    # TODO: Implement this function
    try:
        query = "SELECT * from [cities]"
        cursor = connection.cursor()
        cursor.row_factory= sqlite3.Row
        results = cursor.execute(query)
        my_results = ""
        for row in results:
            print(f"City Id: {row['id']} --City Name: {row['name']} -- Country Id: {row['country_id']}")
            my_results += f"City Id: {row['id']} --City Name: {row['name']} -- Country Id: {row['country_id']}\n"
            
    except sqlite3.OperationalError as ex:
        print(ex)
    return my_results


'''
Good
'''
def average_annual_temperature(connection, city_id, year):
    # TODO: Implement this function
    try:
        query = "SELECT AVG(mean_temp) as avg_temp FROM daily_weather_entries WHERE city_id = ? AND strftime('%Y', date) = ?"
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        result = cursor.execute(query, (city_id, str(year)))
        # Fetch the result
        avg_temp_dict = result.fetchone()
        
        # check if result is not None before accessing
        if avg_temp_dict is not None:
            avg_temp = avg_temp_dict['avg_temp']
            print(f"Average Annual Temperature for City {city_id} in {year}: {avg_temp:.2f}°C")
        else:
            print(f"No data found for City {city_id} in {year}")

    except sqlite3.OperationalError as ex:
        print(ex)
    return f"Average Annual Temperature for City {city_id} in {year}: {avg_temp:.2f}°C"


def average_seven_day_precipitation(connection, city_id, start_date):
    # TODO: Implement this function
    try:
        query = "SELECT AVG(precipitation) as avg_precipitation FROM daily_weather_entries WHERE city_id = ? AND date BETWEEN ? AND date(datetime(?, '+6 days'))"
        # Get a cursor object from database
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        result = cursor.execute(query, (city_id, start_date, start_date))

        # Fetch the result
        avg_precipitation = result.fetchone()['avg_precipitation']
        print(f"Average 7-Day Precipitation for City {city_id} starting from {start_date}: {avg_precipitation:.2f} mm")
    
    except sqlite3.OperationalError as ex:
        print(ex)
    return f"Average 7-Day Precipitation for City {city_id} starting from {start_date}: {avg_precipitation:.2f} mm"

'''
Very good
'''
def average_mean_temp_by_city(connection, date_from, date_to):
    # TODO: Implement this function
    try:
        query = "SELECT city_id, AVG(mean_temp) as avg_temp FROM daily_weather_entries WHERE date BETWEEN ? AND ? GROUP BY city_id"
        # Get a cursor object from database connection
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        result = cursor.execute(query, (date_from, date_to))
        avg_temps = result.fetchall()
        my_results = ""
        for row in avg_temps:
            print(f"Average Temperature for City {row['city_id']} from {date_from} to {date_to}: {row['avg_temp']:.2f}°C")
            my_results += f"Average Temperature for City {row['city_id']} from {date_from} to {date_to}: {row['avg_temp']:.2f}°C\n"

    except sqlite3.OperationalError as ex:
        print(ex)
    
    return my_results

def average_annual_precipitation_by_country(connection, year):
    # TODO: Implement this function
    try:
        query = "SELECT countries.id as country_id, countries.name as country_name, AVG(daily_weather_entries.precipitation) as avg_precipitation "\
            "FROM daily_weather_entries "\
            "JOIN cities ON daily_weather_entries.city_id = cities.id "\
            "JOIN countries ON cities.country_id = countries.id " \
            "WHERE strftime('%Y', date) = ? " \
            "GROUP BY countries.id"
        # Get a cursor object from the database connection
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        # Execute the query via the cursor object
        result = cursor.execute(query, (str(year),))

        # Fetch the results
        avg_precipitations = result.fetchall()
        
        my_results = ""
        for row in avg_precipitations:
            print(f"Average Annual Precipitation for Country {row['country_name']} in {year}: {row['avg_precipitation']:.2f} mm")
            my_results += f"Average Annual Precipitation for Country {row['country_name']} in {year}: {row['avg_precipitation']:.2f} mm\n"

    except sqlite3.OperationalError as ex:
        print(ex)
        
    return my_results

'''
Excellent

You have gone beyond the basic requirements for this aspect.

'''

if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    conn = sqlite3.connect('db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db')
    
    print("All Countries:")
    select_all_countries(conn)
    
    print("\nAll Cities:")
    select_all_cities(conn)

    # example usage for average_annual_temperature
    print("\nAverage Annual Temperature:")
    average_annual_temperature(conn, 1, 2020)
    # Example usage for average_seven_day_precipitation
    print("\nAverage 7-Day Precipitation:")
    average_seven_day_precipitation(conn, 1, '2020-01-01')
    # Example usage for average_mean_temp_by_city
    print("\nAverage Mean Temperature by City:")
    average_mean_temp_by_city(conn, '2020-01-01', '2020-12-31')
    
    # Example usage for average_annual_precipitation_by_country
    print("\nAverage Annual Precipitation by Country:")
    average_annual_precipitation_by_country(conn, 2020)
    
    # Close the database connection
    conn.close()
