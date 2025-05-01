# perform time-taking task on click
from shiny import App, render, ui, reactive

app_ui = ui.page_fluid(
    ui.output_text_verbatim("text_output"),
    ui.input_action_button("click_it", "get data!")
)

def server(input, output, session):
    import pyodide.http

    times = reactive.value( [ ] )

    @reactive.calc
    async def get_time():
        try:
            url = "https://timeapi.io/api/time/current/zone?timeZone=Europe%2FLondon"
            response = await pyodide.http.pyfetch(url)
            time_dict = await response.json()
            return time_dict['dateTime']
        except:
            return "there was a problem"
    
    @reactive.effect
    @reactive.event(input.click_it)
    async def add_new_time():
        new_time = await get_time( )
        times.set(  times( ) + [new_time]  )
    
    @render.text
    def text_output():
        return "\n".join( times( ) )

app = App(app_ui, server)
