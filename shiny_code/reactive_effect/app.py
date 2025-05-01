# shiny @reactive.calc
from shiny import App, render, ui, reactive

app_ui = ui.page_fluid(
    ui.input_slider("slider_1", "Slider value", min=0, max=100, value=10),
    ui.input_action_button("calculate_it", "Perform calculation!"),
)

def server(input, output, session):
    @reactive.effect
    @reactive.event(input.calculate_it)
    def print_some_details():
        print(f"you clicked! Slider showed {input.slider_1()}")

    @reactive.effect
    @reactive.event(input.calculate_it)
    def save_to_database():
        # TODO: here you would save to db
        print(f"Saved {input.slider_1()} do DB")
    

    def print_do_something_else():
        save_to_database(input.slider_1())
    



app = App(app_ui, server)
