from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.input_slider("investment", "N", 0, 100, 20),
    ui.output_text_verbatim("earnings")
)
def server(input, output, session):
    @output
    @render.text
    def earnings():
        new_number = input.investment() *2
        return f"2*n is {new_number}"
        
app = App(app_ui, server)
