from shiny import App, render, ui, reactive
import pandas as pd
from io import StringIO
import pyodide.http
import matplotlib

app_ui = ui.page_fluid(
    ui.input_slider("year_slider",label="choose year", min=2010, max=2021,value=2015, sep=""),
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
        response = await pyodide.http.pyfetch(file_url) # load file
        data = await response.string() # make it a string
        loaded_df = pd.read_csv(StringIO(data)) # read string as csv
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

    # example table:
    @output
    @render.table
    def table_all_data():
        # these first two lines you'll need to put everywhere you are using the data. Then use the variable loaded_df
        global deaths_df
        loaded_df = deaths_df.get()

        demo_countries = ['Ireland', 'India']
        demo_columns = ['country','Immunisation: Hepatitis B_% of children immunised']
        
        return loaded_df[ (loaded_df['year'] == input.year_slider())][(loaded_df['country'].isin(demo_countries))][demo_columns]

app = App(app_ui, server)
