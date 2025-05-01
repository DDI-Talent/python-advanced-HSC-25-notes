# when app loads, ask for time
from shiny import App, render, ui, reactive
import pyodide.http    

app_ui = ui.page_fluid(
    ui.output_text("text_output"),
    ui.input_action_button("refresh_it", "get data!"),
    ui.input_action_button("cancel_it", "cancel request!")
)

def server(input, output, session):
    @ui.bind_task_button(button_id="refresh_it")
    @reactive.extended_task
    async def get_time():
        try:
            url = "https://timeapi.io/api/time/current/zone?timeZone=Europe%2FLondon"
            response = await pyodide.http.pyfetch(url)
            time_dict = await response.json()
            return time_dict['dateTime']
        except:
            return "there was a problem"
            
    @reactive.effect
    @reactive.event(input.refresh_it, ignore_none=False)
    def handle_start():
        get_time()

    @reactive.effect
    @reactive.event(input.cancel_it)
    def handle_cancel():
        get_time.cancel()

    @render.text
    def text_output():
        return str(get_time.result())

app = App(app_ui, server)