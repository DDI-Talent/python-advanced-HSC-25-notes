# shiny @reactive.value
from shiny import App, render, ui, reactive

app_ui = ui.page_fluid(
    ui.input_action_button("click_it", "Click me!"),
    ui.output_text_verbatim("some_result"),
)

def server(input, output, session):
    import random
    random_nums = reactive.value( [ ] )
    
    @reactive.effect
    @reactive.event(input.click_it)
    def _():
        new_number = random.random()
        random_nums.set(  random_nums( ) + [str(new_number)]  )
    
    @render.text
    def some_result():
        print(random_nums( ) )
        return "\n".join( random_nums( ) )

app = App(app_ui, server)
