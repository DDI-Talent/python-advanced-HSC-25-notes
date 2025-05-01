# shiny @reactive.calc
from shiny import App, render, ui, reactive

app_ui = ui.page_fluid(
    ui.input_slider("slider_1", "x 1", min=0, max=10, value=5),
    ui.input_slider("slider_10", "x10", min=0, max=10, value=5),
    ui.output_text("difference_as_text"),
    ui.output_text("difference_as_comparison"),
)

def server(input, output, session):
    import pyodide.http

    @reactive.calc
    def sliders_difference():
      return input.slider_1() - input.slider_10()
    
    @render.text
    def difference_as_text():
      return f"Difference is { sliders_difference( ) }"
    
    @render.text
    def difference_as_comparison():
        larger_one = "first" if int(sliders_difference( )) > 0 else "second"  
        return f"{larger_one} is larger"


app = App(app_ui, server)
