from shiny import App, render, ui, reactive
import pandas as pd
from io import StringIO
import pyodide.http
import matplotlib

app_ui = ui.page_fluid(
    ui.input_slider("year_slider",label="choose year", min=2010, max=2021,value=2015, sep=""),
    ui.output_plot("plot_test"),
    ui.output_table("table_all_data")
)

def server(input, output, session):
    # done for you - reactive data variables
    global deaths_df
    deaths_df = reactive.value(pd.DataFrame({}))

    async def parsed_data_from_url():
        # done for you - get online data
        global deaths_df
        file_url = "https://raw.githubusercontent.com/drpawelo/data/main/health/OCED_simplified.csv"
        response = await pyodide.http.pyfetch(file_url)
        data = await response.string()
        loaded_df = pd.read_csv(StringIO(data))
        return loaded_df

    # here reactive.Effect means that the function is ran once, at the beginning.
    @reactive.Effect 
    async def refreshData():
        # done for you - making sure online data is being up to date
        global deaths_df
        data_so_far = deaths_df.get()
        if data_so_far.empty == True:
            print("started loading online data")
            deaths_df.set(await parsed_data_from_url())
            print("finished loading online data")
        else:
            print("online data was already loaded")

    # example helper function:
    def just_data_for_selected_year( input_data_df ):
        # take data, filter then, then return what's left. This can be used for longer operations too
        # eg. to only keep some columns, or rows
        return input_data_df[ (input_data_df['year'] == input.year_slider())]
        
    
    # example graph:
    @output
    @render.plot
    async def plot_test():
        # these first two lines you'll need to put everywhere you are using the data. Then use the variable loaded_df
        global deaths_df
        loaded_df = deaths_df.get()

        demo_columns = [
                        'country',
                        'Immunisation: Hepatitis B_% of children immunised',
                        'Immunisation: Measles_% of children immunised']

        demo_countries = ['Ireland', 'Italy']
        
        # for example: this starting code keeps only data for selected year, some countries and columns
        
        data_for_year = just_data_for_selected_year(loaded_df) # filtering can be outsourced to a function
        subset_of_data = data_for_year[(loaded_df['country'].isin(demo_countries)) ] # od done right here
        
        plot = subset_of_data[demo_columns].plot(x='country', kind='bar') # here we make a graph
        plot.legend(loc='lower center') # and tweak it
        return plot

    # example graph:
    @output
    @render.table
    def table_all_data():
        # these first two lines you'll need to put everywhere you are using the data. Then use the variable loaded_df
        global deaths_df
        loaded_df = deaths_df.get()

        demo_columns = [
                        'country',
                        'Immunisation: Hepatitis B_% of children immunised',
                        'Immunisation: Measles_% of children immunised']

        demo_countries = ['Ireland', 'India', 'Italy', 'Iceland']
        return loaded_df[ (loaded_df['year'] == input.year_slider()) & (loaded_df['country'].isin(demo_countries)) ][demo_columns]

app = App(app_ui, server)
