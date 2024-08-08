import sqlite3
import matplotlib.pyplot as plt

# Connect to the SQLite database
def connect_to_database(database_name):
    connection = sqlite3.connect(database_name)
    return connection

# Close the database connection
def close_connection(connection):
    connection.close()

# Query 1: Select all cities
def select_all_cities(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT cities.name FROM cities;")
    result = cursor.fetchall()
    return result

# Query 2: Select all cities with their respective data
def select_all_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM daily_weather_entries;")
    result = cursor.fetchall()
    return result

# Query 3: Select average annual temperature
def select_average_annual_temperature(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT AVG(mean_temp) FROM daily_weather_entries;")
    result = cursor.fetchone()[0]
    return result

# Query 4: Select average seven-day precipitation
def select_average_seven_day_precipitation(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT AVG(precipitation) FROM daily_weather_entries;")
    result = cursor.fetchone()[0]
    return result

# Query 5: Select average mean temperature by city
def select_average_mean_temperature_by_city(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT cities.name, AVG(daily_weather_entries.mean_temp) 
        FROM cities 
        JOIN daily_weather_entries ON cities.id = daily_weather_entries.city_id 
        GROUP BY cities.name;
    """)
    result = cursor.fetchall()
    return result

# Query 6: Select average annual precipitation
def select_average_annual_precipitation(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT AVG(daily_weather_entries.precipitation) FROM daily_weather_entries;")
    result = cursor.fetchone()[0]
    return result

# Query 7: Select average precipitation by city
def select_average_precipitation_by_city_and_date_range(connection, start_date, end_date):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT cities.name, AVG(daily_weather_entries.precipitation) 
        FROM cities 
        JOIN daily_weather_entries ON cities.id = daily_weather_entries.city_id 
        WHERE daily_weather_entries.date BETWEEN ? AND ?
        GROUP BY cities.name;
    """, (start_date, end_date))
    result = cursor.fetchall()
    return result

# Query 8: Select min and max temperature by city for a particular time range
def select_min_max_temperature_by_city_and_date_range(connection, city_name, start_date, end_date):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT daily_weather_entries.date, 
               MIN(daily_weather_entries.min_temp) AS min_temp, 
               MAX(daily_weather_entries.max_temp) AS max_temp,
               AVG(daily_weather_entries.mean_temp) AS mean_temp,
               AVG(daily_weather_entries.precipitation)
        FROM cities 
        JOIN daily_weather_entries ON cities.id = daily_weather_entries.city_id 
        WHERE cities.name = ? AND daily_weather_entries.date BETWEEN ? AND ?
        GROUP BY daily_weather_entries.date;
    """, (city_name, start_date, end_date))
    result = cursor.fetchall()
    return result

def delete_data_by_city_id_and_date_range(connection, city_id, start_date, end_date):
    try:
        cursor = connection.cursor()

        # Delete data by city_name and date range
        cursor.execute("""
                       DELETE FROM daily_weather_entries
                       WHERE city_id = ? AND date BETWEEN ? AND ?""", (city_id, start_date, end_date))
        connection.commit()
    except sqlite3.Error as e:
        print("Error deleting data:", e)
    finally:
        cursor.close()

def delete_all_data(connection):
    try:
        cursor = connection.cursor()

        # Delete all data
        cursor.execute("DELETE FROM daily_weather_entries")
        
        connection.commit()
    except sqlite3.Error as e:
        print("Error deleting all data:", e)
    finally:
        cursor.close()

def plot_7_day_precipitation(avg_seven_day_precip):
    # Extracting city names and precipitation values from the result
    cities = [row[0] for row in avg_seven_day_precip]
    precipitation_values = [row[1] for row in avg_seven_day_precip]

    # Plotting the bar chart
    plt.bar(cities, precipitation_values, color='blue')
    plt.xlabel('City')
    plt.ylabel('Average 7-Day Precipitation')
    plt.title('Average 7-Day Precipitation by City')
    plt.show()

def plot_grouped_bar_chart(temperature_data, precipitation_data):
    # Assuming temperature_data and precipitation_data are results from relevant functions

    # Extracting data for plotting
    cities = [row[0] for row in temperature_data]
    min_temps = [row[1] for row in temperature_data]
    max_temps = [row[2] for row in temperature_data]
    mean_temps = [row[3] for row in temperature_data]
    precipitation_values = [row[1] for row in precipitation_data]

    # Setting the bar width
    bar_width = 0.2
    bar_distance = 0.15

    # Plotting the grouped bar chart
    fig, ax = plt.subplots()
    index = range(len(cities))
    bar1 = ax.bar(index, min_temps, bar_width, label='Min Temperature')
    bar2 = ax.bar([i + bar_width for i in index], max_temps, bar_width, label='Max Temperature')
    bar3 = ax.bar([i + 2 * bar_width for i in index], mean_temps, bar_width, label='Mean Temperature')

    ax.set_xlabel('City')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Min/Max/Mean Temperature by City')
    ax.set_xticks([i + (bar_width + bar_distance) for i in index])
    ax.set_xticklabels(cities)
    ax.legend()
    plt.xticks(rotation=90, fontsize=5)

    plt.show()

def plot_multiline_chart(min_max_temp_data, city_name, month=""):
    # Assuming min_max_temp_data is the result from select_min_max_temperature_by_city_and_date_range

    # Extracting data for plotting
    dates = [row[0] for row in min_max_temp_data]
    min_temps = [row[1] for row in min_max_temp_data]
    max_temps = [row[2] for row in min_max_temp_data]

    # Plotting the multi-line chart
    plt.plot(dates, min_temps, label='Min Temperature')
    plt.plot(dates, max_temps, label='Max Temperature')

    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Daily Min/Max Temperature for {city_name} - {month}')
    plt.xticks(rotation=90, fontsize=5)
    plt.legend()
    plt.show()

def scatter_plot_mean_temperature_vs_precipitation_for_cities(city_name, mean_temp_data, avg_precip_data):
    # mean_temp_data and avg_precip_data should be results from relevant functions for cities

    # Extracting data for plotting
    dates = [row[0] for row in mean_temp_data]
    mean_temps = [row[3] for row in mean_temp_data]
    avg_precipitations = [row[4] for row in avg_precip_data]

    # Plotting the scatter plot chart
    plt.scatter(mean_temps, avg_precipitations, label='Data Points')

    # Adding labels and title
    plt.xlabel('Mean Temperature (°C)')
    plt.ylabel('Average Precipitation (mm)')
    plt.title('Mean Temperature vs Average Precipitation for {city_name}')

    # Adding labels for each point
    for i, date in enumerate(dates):
        plt.annotate(date, (mean_temps[i], avg_precipitations[i]))

    # Display the legend
    plt.legend()

    # Show the plot
    plt.show()

# Example usage:
database_name = "db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
connection = connect_to_database(database_name)

# Call the functions based on your requirements
cities = select_all_cities(connection)
all_data = select_all_data(connection)
avg_annual_temp = select_average_annual_temperature(connection)
avg_seven_day_precip = select_average_seven_day_precipitation(connection)
avg_mean_temp_by_city = select_average_mean_temperature_by_city(connection)
avg_annual_precip = select_average_annual_precipitation(connection)


# specify date range
city_name = "Middlesbrough"
start_date = "2021-01-04"
end_date = "2021-01-31"
# Call the function to get average precipitation by city for the specified time range
avg_precip_by_city_and_date_range = select_average_precipitation_by_city_and_date_range(connection, start_date, end_date)
avg_precip_by_city = select_min_max_temperature_by_city_and_date_range(connection, city_name, start_date, end_date)

min_max_temp_by_city_and_date_range = select_min_max_temperature_by_city_and_date_range(connection, city_name, start_date, end_date)

# Close the connection after use
close_connection(connection)

# Print or use the results as needed
print("All Cities:", cities)
print("All Data:", all_data)
print("Average Annual Temperature:", avg_annual_temp)
print("Average Seven-Day Precipitation:", avg_seven_day_precip)
print("Average Mean Temperature by City:", avg_mean_temp_by_city)
print("Average Annual Precipitation:", avg_annual_precip)
print(f"Average Precipitation by City for {start_date} to {end_date}:", avg_precip_by_city_and_date_range)
print(f"Min and Max Temperature for {city_name} from {start_date} to {end_date}:")
for row in min_max_temp_by_city_and_date_range:
    if row is not None:
        print(f"Date: {row[0]}, Min Temperature: {row[1]}, Max Temperature: {row[2]} Mean Temperature: {row[3]}")
    else:
        print("No data for specified date.")

plot_7_day_precipitation(avg_precip_by_city_and_date_range)
plot_grouped_bar_chart(min_max_temp_by_city_and_date_range, avg_precip_by_city_and_date_range)
plot_multiline_chart(min_max_temp_by_city_and_date_range, city_name, "January")
scatter_plot_mean_temperature_vs_precipitation_for_cities(city_name, min_max_temp_by_city_and_date_range, avg_precip_by_city)
