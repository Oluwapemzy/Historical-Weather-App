import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry #import pip install ..
from phase_1 import select_all_countries, select_all_cities, average_annual_temperature, average_seven_day_precipitation, average_mean_temp_by_city, average_annual_precipitation_by_country
from phase_2 import (connect_to_database, close_connection, select_average_annual_temperature, select_average_seven_day_precipitation, select_average_mean_temperature_by_city, select_average_annual_precipitation, select_average_precipitation_by_city_and_date_range, select_min_max_temperature_by_city_and_date_range, plot_7_day_precipitation, plot_grouped_bar_chart, plot_multiline_chart, scatter_plot_mean_temperature_vs_precipitation_for_cities, delete_data_by_city_id_and_date_range, delete_all_data
)

class DatabaseQueryApp:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Database Query App")


        # Create a StringVar to store the selected query
        self.selected_query = tk.StringVar()
        self.city_id_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        # self.chart_type_var = tk.StringVar()
        self.city_name_var = tk.StringVar()

        # Create and set up the UI components
        self.city_name_label = None
        self.city_name_entry = None
        # self.chart_type_label = None
        # self.chart_type_combobox = None
        self.city_id_label = None
        self.city_id_entry = None
        self.year_label = None
        self.year_entry = None
        self.start_date_label = None
        self.start_date_combobox = None
        self.end_date_label = None
        self.end_date_combobox = None

        self.create_ui()

    def create_ui(self):
        # Label and Combobox for selecting the query
        query_label = tk.Label(self.root, text="Select Query:")
        query_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W)

        query_combobox = ttk.Combobox(self.root, textvariable=self.selected_query, values=[
            "Select Query",
            "All Countries",
            "All Cities",
            "Average Annual Temperature",
            "Average Seven Day Precipitation",
            "Average Mean Temperature by City",
            "Average Annual Precipitation by Country",
            "Average Precipitation by City and Date Range",
            "Min/Max Temperature by City and Date Range",
            "Plot 7-Day Precipitation",
            "Plot Grouped Bar Chart",
            "Plot Multiline Chart",
            "Scatter Plot: Mean Temp vs. Precipitation",
            "Delete Data by City and Date Range",
            "Delete All Data"
        ])
        query_combobox.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)
        query_combobox.current(0)  # Set the default value
        
        # Bind the callback method to the Combobox selection
        query_combobox.bind("<<ComboboxSelected>>", self.on_query_selection)
        
        # Entry widgets for city_id and year
        self.city_id_label  = tk.Label(self.root, text="City ID:")
        self.city_id_label.grid(row=1, column=0, pady=5, padx=10, sticky=tk.W)

        self.city_id_entry = tk.Entry(self.root, textvariable=self.city_id_var)
        self.city_id_entry.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)

        self.year_label =tk.Label(self.root, text="Year:")
        self.year_label.grid(row=2, column=0, pady=5, padx=10, sticky=tk.W)

        self.year_entry = tk.Entry(self.root, textvariable=self.year_var)
        self.year_entry.grid(row=2, column=1, pady=5, padx=10, sticky=tk.W)
        
        # Combobox for selecting the start date
        self.start_date_label = tk.Label(self.root, text="Start Date:")
        self.start_date_label.grid(row=3, column=0, pady=5, padx=10, sticky=tk.W)

        self.start_date_combobox = DateEntry(self.root, textvariable=self.start_date_var, date_pattern="yyyy-mm-dd")
        self.start_date_combobox.grid(row=3, column=1, pady=5, padx=10, sticky=tk.W)
        
        # Combobox for selecting the end date
        self.end_date_label = tk.Label(self.root, text="End Date:")
        self.end_date_label.grid(row=4, column=0, pady=5, padx=10, sticky=tk.W)

        self.end_date_combobox = DateEntry(self.root, textvariable=self.end_date_var, date_pattern="yyyy-mm-dd")
        self.end_date_combobox.grid(row=4, column=1, pady=5, padx=10, sticky=tk.W)
        
        self.city_name_label  = tk.Label(self.root, text="City Name:")
        self.city_name_label.grid(row=6, column=0, pady=5, padx=10, sticky=tk.W)

        self.city_name_entry = tk.Entry(self.root, textvariable=self.city_name_var)
        self.city_name_entry.grid(row=6, column=1, pady=5, padx=10, sticky=tk.W)

        # Button to execute the selected query
        execute_button = tk.Button(self.root, text="Execute Query", command=self.execute_query)
        execute_button.grid(row=8, column=0, columnspan=1, pady=10, padx=10)
        
        # Button to delete data
        delete_button  = tk.Button(
            self.root, text="Delete Data", command=self.delete_data
        )
        delete_button.grid(row=8, column=2, columnspan=2, pady=10, padx=10)
        
        # Button to quit the application
        quit_button = tk.Button(self.root, text="Quit Application", command=self.root.quit)
        quit_button.grid(row=10, column=1, columnspan=2, pady=10, padx=10)
    
    def delete_data(self):
        selected_query = self.selected_query.get()
        if selected_query == "Delete Data by City and Date Range":
            delete_data_by_city_id_and_date_range(
                self.connection,
                self.city_id_var.get(),
                self.start_date_var.get(),
                self.end_date_var.get(),
            )
            messagebox.showinfo("Delete Result", "Data deleted successfully.")
        elif selected_query == "Delete All Data":
            delete_all_data(self.connection)
            messagebox.showinfo("Delete Result", "All data deleted successfully.")
        else:
            messagebox.showinfo("Error", "Please select a valid delete option.")


    def on_query_selection(self, event):
        selected_query = self.selected_query.get()

        # Hide all input widgets initially
        self.hide_all_widgets()

        # show input widgets based on the selected query
        if selected_query == "Average Annual Temperature":
           self.show_widgets([self.city_id_label, self.year_label, self.year_entry, self.city_id_entry]) 
        elif selected_query == "Average Seven Day Precipitation":
            self.show_widgets([self.city_id_label, self.start_date_label, self.city_id_entry, self.start_date_combobox])
            self.show_widgets([self.end_date_label, self.end_date_combobox])
        elif selected_query == "Average Mean Temperature by City":
            self.show_widgets([ self.start_date_label, self.end_date_label, self.start_date_combobox, self.end_date_combobox])
        elif selected_query == "Average Annual Precipitation by Country":
            self.show_widgets([self.year_label, self.year_entry])
        elif selected_query == "Average Precipitation by City and Date Range":
            self.show_widgets([self.start_date_label, self.end_date_label, self.end_date_combobox, self.start_date_combobox])
        elif selected_query =="Min/Max Temperature by City and Date Range":
            self.show_widgets([self.city_name_label, self.city_name_entry, self.start_date_label, self.start_date_combobox, self.end_date_label, self.end_date_combobox])
        elif selected_query == "Plot 7-Day Precipitation":
            self.show_widgets([self.start_date_label, self.start_date_combobox, self.end_date_label, self.end_date_combobox])
        elif selected_query == "Plot Grouped Bar Chart":
            self.show_widgets([self.start_date_label, self.start_date_combobox, self.end_date_label, self.end_date_combobox, self.city_name_label, self.city_name_entry])
        elif selected_query == "Plot Multiline Chart":
            self.show_widgets([self.city_name_label, self.city_name_entry, self.start_date_label, self.start_date_combobox, self.end_date_label, self.end_date_combobox])
        elif selected_query == "Scatter Plot: Mean Temp vs. Precipitation":
            self.show_widgets([self.city_name_label, self.city_name_entry, self.start_date_label, self.start_date_combobox, self.end_date_label, self.end_date_combobox])

    def show_widgets(self, widgets):
        for widget in widgets:
            widget.grid()
    
    def hide_all_widgets(self):
        for widget in [
            self.city_id_label, self.city_id_entry,self.year_label, self.year_entry,
            self.start_date_label, self.start_date_combobox, self.end_date_label, 
            self.end_date_combobox, self.city_name_label, self.city_id_entry, self.city_name_entry
        ]:
            widget.grid_remove() #, self.chart_type_label, self.chart_type_combobox

    def execute_query(self):
        # Get the selected query
        selected_query = self.selected_query.get()
        
        # Execute the corresponding database query function
        if selected_query == "All Countries":
            result = select_all_countries(self.connection)
        elif selected_query == "All Cities":
            result = select_all_cities(self.connection)
        else:
            # Get city_id and year from Entry Widgets
            city_id = self.city_id_var.get()
            city_name = self.city_name_var.get()
            year = self.year_var.get()
            start_date = self.start_date_var.get()
            end_date = self.end_date_var.get()

            # Validate that city_id and year are not empty
            if not self.validate_inputs(selected_query, city_id, year, start_date, end_date, city_name):
                messagebox.showinfo("Error", "Please enter values for City ID, Year, City Name, Start Date and End date.")
                return

            # Execute the corresponding database query function
            
            if selected_query == "Average Annual Temperature":
                result = average_annual_temperature(self.connection, city_id, year)
            elif selected_query == "Average Seven Day Precipitation":
                result = average_seven_day_precipitation(self.connection, city_id, start_date)
            elif selected_query == "Average Mean Temperature by City":
                result = average_mean_temp_by_city(self.connection, start_date, end_date)
            elif selected_query == "Average Annual Precipitation by Country":
                result = average_annual_precipitation_by_country(self.connection, year)
            elif selected_query == "Average Precipitation by City and Date Range":
                result = select_average_precipitation_by_city_and_date_range(self.connection, self.start_date_var.get(), self.end_date_var.get())
            elif selected_query == "Min/Max Temperature by City and Date Range":
                result = select_min_max_temperature_by_city_and_date_range(self.connection, self.city_name_var.get(), self.start_date_var.get(), self.end_date_var.get())
                
            elif selected_query == "Plot 7-Day Precipitation":
                pre_result = select_average_precipitation_by_city_and_date_range(self.connection, self.start_date_var.get(), self.end_date_var.get())
                plot_7_day_precipitation(pre_result)
                return
            elif selected_query == "Plot Grouped Bar Chart":
                pre_result_precip = select_average_precipitation_by_city_and_date_range(self.connection, self.start_date_var.get(), self.end_date_var.get())
                pre_result_min_max = select_min_max_temperature_by_city_and_date_range(self.connection, self.city_name_var.get(), self.start_date_var.get(), self.end_date_var.get())
                plot_grouped_bar_chart(pre_result_min_max, pre_result_precip)
                return
            elif selected_query == "Plot Multiline Chart":
                pre_result_min_max = select_min_max_temperature_by_city_and_date_range(self.connection, self.city_name_var.get(), self.start_date_var.get(), self.end_date_var.get())
                plot_multiline_chart(pre_result_min_max, self.city_name_var.get())
                return
            elif selected_query == "Scatter Plot: Mean Temp vs. Precipitation":
                pre_mean_data = select_min_max_temperature_by_city_and_date_range(self.connection, self.city_name_var.get(), self.start_date_var.get(), self.end_date_var.get())
                pre_precip_data = pre_mean_data
                scatter_plot_mean_temperature_vs_precipitation_for_cities(self.city_name_var.get(), pre_mean_data, pre_precip_data)
                return

            else:
                result = "Invalid query"
                messagebox.showinfo("Error", "Please select a valid query.")
                return

        # Display the result in a messagebox
        messagebox.showinfo("Query Result", result)

    def validate_inputs(self, selected_query, city_id, year, start_date, end_date, city_name):
        # Implement Validation logic based on the selected query
        if selected_query == "Average Annual Temperature":
           if not city_id or not year:
                messagebox.showinfo("Error", "Please enter values for City ID and Year")
                return False
        elif selected_query == "Average Seven Day Precipitation":
            if not city_id or not start_date or not end_date:
                messagebox.showinfo("Error", "Please enter values for City ID, Start Date, and End Date.")
                return False
        elif selected_query == "Average Mean Temperature by City":
            if not start_date or not end_date:
                messagebox.showinfo("Error", "Please enter values for Start Date, and End Date.")
                return False
        elif selected_query == "Average Annual Precipitation by Country":
            if not year:
                messagebox.showinfo("Error", "Please enter a value Year")
                return False
        elif selected_query == "Average Precipitation by City and Date Range":
            if not start_date or not end_date:
                messagebox.showinfo("Error", "Please enter values for Start Date, and End Date.")
                return False
        elif selected_query == "Min/Max Temperature by City and Date Range":
            if not city_name or not start_date or not end_date:
                messagebox.showinfo("Error", "Please enter values for City Name, Start Date, and End Date")
                return False
        elif selected_query == "Plot 7-Day Precipitation":
            if  not start_date or not end_date:
                messagebox.showinfo("Error", "Please enter values for Start Date, and End Date.")
                return False
        elif selected_query == "Plot Grouped Bar Chart":
            if not city_name or not start_date or not end_date:
                messagebox.showinfo("Error", "Please enter values for City Name, Start Date, and End Date")
                return False             
        elif selected_query == "Plot Multiline Chart":
               if not city_name or not start_date or not end_date:
                    messagebox.showinfo("Error", "Please enter values for City Name, Start Date, and End Date")
                    return False                   
        elif selected_query == "Scatter Plot: Mean Temp vs. Precipitation":
            if not city_name or not start_date or not end_date:
                messagebox.showinfo("Error", "Please enter values for City Name, Start Date, and End Date")
                return False
        else:
            messagebox.showinfo("Error", f"Invalid query: {selected_query}")
            return False
        return True

if __name__ == "__main__":
    connection = connect_to_database("db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db")
    root = tk.Tk()
    app = DatabaseQueryApp(root, connection)
    root.mainloop()
    close_connection(connection)
