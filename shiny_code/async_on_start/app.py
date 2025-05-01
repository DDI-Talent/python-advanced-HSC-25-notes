# when app loads, ask some website for time
from shiny import App, render, ui, reactive

app_ui = ui.page_fluid(
    ui.output_text("text_output"),
)

def server(input, output, session):
    
    import pyodide.http    
    @reactive.calc
    async def get_time():
        try:
            url = "https://timeapi.io/api/time/current/zone?timeZone=Europe%2FLondon"
            response = await pyodide.http.pyfetch(url)
            time_dict = await response.json()
            return time_dict['dateTime']
        except:
            return "there was a problem"
    
    @render.text
    async def text_output():
        time = await get_time()
        return f"time now: {time}"


app = App(app_ui, server)