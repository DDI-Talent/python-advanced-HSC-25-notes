# shiny @reactive.calc
from shiny import App, render, ui, reactive

app_ui = ui.page_fluid(
    ui.input_action_button("click_it", "Click me!"),
    ui.output_text("some_result"),
)

def server(input, output, session):
    times_clicked = reactive.value( 0 )
        
    @reactive.effect
    @reactive.event(input.click_it)
    def _():
        new_click_count = times_clicked() + 1
        times_clicked.set( new_click_count  )
    
    @render.text
    def some_result():
        return f"current count { times_clicked( ) }"

app = App(app_ui, server)
